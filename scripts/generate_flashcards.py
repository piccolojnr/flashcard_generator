import os
import json
from tqdm import tqdm
import requests
from scripts import caching

# Define the base directory for API URL and other paths
API_URL = "http://127.0.0.1:11434/api/generate"
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))


def get_prompt(data):
    default_prompt = """Instructions:
1. Review the text carefully.
2. Identify key concepts, important definitions, and significant facts.
3. For each key point, generate a question that prompts recall or understanding.
4. Make sure each question has a clear and concise answer derived from the text.
5. Include additional relevant information if necessary to provide context or enhance understanding.
6. Format the flashcards into JSON, with each flashcard containing a question and its corresponding answer.
7. Ensure that the JSON structure follows the format: [{"question": "Question text", "answer": "Answer text"}, ...]
8. Aim for clarity and simplicity in both questions and answers."""
    return f"{data}\n{default_prompt}"


def extract_list(data):
    extracted = []
    if isinstance(data, dict):
        for key, value in data.items():
            extracted.extend(extract_list(value))
    elif isinstance(data, list):
        for item in data:
            extracted.extend(extract_list(item))
    elif isinstance(data, dict) and "question" in data and "answer" in data:
        extracted.append(data)
    return extracted


def post(url, data):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error during API request: {e}")
        return None


def get_flashcards_data(data, model="llama3"):
    response = post(
        API_URL,
        {
            "model": model,
            "prompt": get_prompt(data),
            "stream": False,
            "format": "json",
        },
    )
    if response and "response" in response:
        return response["response"]
    else:
        print("Invalid response from API.")
        return None


def generate(debug=False, model=None):
    """
    Generate flashcards from input files.

    Args:
        debug (bool, optional): If True, raise an exception when an error occurs. Defaults to False.
        model: The model to use for generating flashcards. Defaults to None.

    Returns:
        list: A list of file paths where the generated flashcards are saved.
    """
    
    output_path = os.path.join(PROJECT_ROOT, "extracted_json")
    input_path = os.path.join(PROJECT_ROOT, "extracted_data")
    if not os.path.exists(input_path):
        raise FileNotFoundError("Extracted data directory not found.")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    cache_db_path = os.path.join(PROJECT_ROOT, "cache.db")
    caching.init_cache_db(cache_db_path)

    input_files = []
    if os.path.isfile(input_path):
        input_files.append(input_path)
    elif os.path.isdir(input_path):
        input_files.extend(
            [
                os.path.join(input_path, file)
                for file in os.listdir(input_path)
                if file.endswith(".txt")
            ]
        )
    else:
        print("Invalid input path.")
        return

    try:
        files = []
        for file in tqdm(input_files, desc="Processing files"):
            with open(file, "r", encoding="utf-8") as f:
                data = f.read()
            file_hash = caching.generate_sha256(data)
            output_file = os.path.join(output_path, file_hash + ".json")
            file_path = caching.get_file_path_from_cache(cache_db_path, file_hash)
            files.append(output_file)
            if file_path:
                caching.update_file_path_in_cache(cache_db_path, file_hash, output_file)
            else:
                flashcards_data = get_flashcards_data(data, model)
                if flashcards_data:
                    flashcards_data = json.loads(flashcards_data)
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(flashcards_data, f, indent=4)
                        caching.add_file_path_to_cache(
                            cache_db_path, file_hash, output_file
                        )
                else:
                    print(f"Failed to generate flashcards for {file}")
        print(f"Flashcards generated for {len(files)} files.")
        return files
    except Exception as e:
        print(f"An error occurred: {e}")
        if debug:
            raise e

