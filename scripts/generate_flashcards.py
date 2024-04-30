from openai import OpenAI
import os
import json
from tqdm import tqdm

ZUKI_API_KEY = os.getenv("ZUKI_API_KEY")
NAGA_API_KEY = os.getenv("NAGA_API_KEY")
HYZENBERG_API_KEY = os.getenv("HYZENBERG_API_KEY")
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
WEBRAFT_API_KEY = os.getenv("WEBRAFT_API_KEY")
SHUTTLE_API_KEY = os.getenv("SHUTTLE_API_KEY")
OXYGEN_API_KEY = os.getenv("OXYGEN_API_KEY")
MANDRILL_API_KEY = os.getenv("MANDRILL_API_KEY")


def extract_list(response):
    if isinstance(response, list):
        if isinstance(response[0], dict):
            if "question" in response[0].keys() and "answer" in response[0].keys():
                return response
        return []
    elif isinstance(response, dict):
        ss = []
        if "question" in response.keys() and "answer" in response.keys():
            ss.append(response)
        for k, v in response.items():
            if isinstance(v, list):
                if isinstance(v[0], dict):
                    if "question" in v[0].keys() and "answer" in v[0].keys():
                        ss.extend(v)
            elif isinstance(v, dict):
                return extract_list(v)

        return ss

    else:
        return []


def configure_zuki():
    return OpenAI(
        api_key=NAGA_API_KEY,
        base_url="https://zukijourney.xyzbot.net/v1",
    )


def configure_naga():
    return OpenAI(
        base_url="https://api.naga.ac/v1", api_key="ng-qw70virPCYuGF4lH310opCp6JrwV9"
    )


def configure_hyzenberg():
    return OpenAI(
        base_url="https://api.hyzen.cc/v1",
        api_key=HYZENBERG_API_KEY,
    )


def configure_kraken():
    return OpenAI(
        base_url="https://api.cracked.systems/v1",
        api_key=KRAKEN_API_KEY,
    )


def configure_webraft():
    return OpenAI(
        base_url="https://api.webraft.in/freeapi",
        api_key=WEBRAFT_API_KEY,
    )


def configure_shuttle():
    return OpenAI(
        base_url="https://api.shuttleai.app/v1",
        api_key=SHUTTLE_API_KEY,
    )


def configure_mandrill():
    return OpenAI(
        base_url="https://api.mandrillai.tech/v1",
        api_key=MANDRILL_API_KEY,
    )


def configure_oxygen():
    return OpenAI(
        base_url="https://app.oxyapi.uk/v1/",
        api_key=OXYGEN_API_KEY,
    )


CLIENTS = [
    configure_naga(),
    configure_zuki(),
    configure_hyzenberg(),
    configure_kraken(),
    configure_webraft(),
    configure_shuttle(),
    configure_mandrill(),
    configure_oxygen(),
]


def use_ai(client, content):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": content}]
    )
    return response.choices[0].message.content


def get_flashcards_data(data, client, prompt=None):
    prompt = prompt if prompt else "Generate JSON flashcards from the following text:"
    data = f"{prompt}\n{data}"
    content = f"""{data}
Instructions:
1. Review the text thoroughly.
2. Pinpoint key points for flashcards.
3. Generate questions based on these key points.
4. Include additional relevant information if deemed important.
5. Format the flashcards into JSON, incorporating questions and answers."""

    return use_ai(client, content)


def generate(input_path, output_path, prompt=None):
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
        exit()

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        print("Getting flashcards data...")
        for file in tqdm(input_files):
            output_file = os.path.join(
                output_path, os.path.splitext(os.path.basename(file))[0] + ".json"
            )
            if os.path.exists(output_file):
                continue
            with open(file, "r", encoding="utf-8") as f:
                data = f.read()
            while len(CLIENTS) > 0:
                client = CLIENTS[0]
                print(f"Using client: {client.base_url}")
                try:
                    flashcards_data = get_flashcards_data(data, client, prompt=prompt)
                    if flashcards_data is not None:
                        flashcards_data = json.loads(flashcards_data)
                        flashcards_data = extract_list(flashcards_data)
                        with open(output_file, "w", encoding="utf-8") as f:
                            json.dump(flashcards_data, f, indent=4)
                        break  # Stop trying other clients if successful
                except Exception as e:
                    CLIENTS.pop(0)  # Remove failed client
                    print(e)
                    print(f"\nError with client: {client.base_url}")
                    continue  # Try next client if error occurs
            else:
                print("All AI services failed. Please try again later.")
                exit()
        print("All flashcards data saved successfully.")
    except Exception as e:
        import traceback

        traceback.print_exc()
        print("An error occurred. Please check the logs for more information.")
        exit()


def generate_flashcards(prompt=None):
    if not os.path.exists("./extracted_data"):
        raise FileNotFoundError("Extracted data directory not found.")

    generate("./extracted_data", "./flashcard_data", prompt=prompt)


def generate_flashcards_from_args(args):
    generate(args.input, args.output, prompt=args.prompt)
