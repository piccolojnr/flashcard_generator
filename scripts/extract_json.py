from bs4 import BeautifulSoup
import argparse
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = os.getcwd()

def extract_data(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <code> tags with class "json-language"
    json_codes = soup.find_all('code', class_='language-json')

    data = []
    # Extract content and child tags content
    for code in json_codes:
        content = code.get_text(strip=True)
        json_data  = json.loads(content)
        if not isinstance(json_data, list):
            json_data = [json_data]
        data.extend(json_data)
    
    return data

def main(input_path, output_path, merge, limit):
 
    
    input_files = []
    if os.path.isfile(input_path):
        input_files.append(input_path)
    elif os.path.isdir(input_path):
        for file in os.listdir(input_path):
            if file.endswith(".html"):
                input_files.append(os.path.join(input_path, file))
    else:
        print("Invalid input path")
        return

    extracted_data = []
    for input_file in input_files:
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        data = extract_data(html_content)
        extracted_data.extend(data)
    
    if merge:        
        with open(output_path+".json", 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f)
    else:
        if os.path.exists(output_path) and len(os.listdir(output_path)) > 0:
            raise ValueError("Output path is not empty.")
        elif not os.path.exists(output_path):
            os.makedirs(output_path)
        
        for i, j in enumerate(range(0, len(extracted_data), limit)):
            with open(os.path.join(output_path, f"output_{i}.json"), 'w', encoding='utf-8') as f:
                json.dump(extracted_data[j:j+limit], f)
    
    print(f"Output files saved to {output_path}.")
        
    
def extract_json(args):
    try:
        input_path = os.path.join(current_dir, args.input)
        output_path = os.path.join(current_dir, args.output)
        print(input_path)
        if not input_path:
            raise ValueError("Input path is required.")
        if not output_path:
            raise ValueError("Output path is required.")
        if args.merge and args.limit:
            raise ValueError("Cannot merge and limit simultaneously.")
        if not os.path.exists(input_path):
            raise ValueError("Input path does not exist.")

        main(input_path, output_path, args.merge, args.limit)
    except Exception as e:
        import traceback
        traceback.print_exc()
    
    