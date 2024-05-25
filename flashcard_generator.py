#!/usr/bin/env python3
import argparse
from scripts.extract_text import extract
from scripts.generate_flashcards import generate
from scripts.create_presentation import create


def main():
    parser = argparse.ArgumentParser(description="Unified tool for extracting text and generating flashcards.")
    
    parser.add_argument("-i", "--input", help="Path to the input file or directory containing [.pptx, .pdf, .txt, .docx] files.", required=True)
    parser.add_argument("-o", "--output", help="Path to the output directory.", required=True)
    parser.add_argument("-n", "--name", help="Name of the output PowerPoint presentation file (without extension).", required=True)
    parser.add_argument("-t", "--title", help="Title of the output presentation.", required=True)
    parser.add_argument("-m", "--model", help="Specify the AI model to use.", default="llama3")
    parser.add_argument("-d", "--debug", help="Enable debug mode.", action="store_true")
    
    args = parser.parse_args()
    
    input_path = args.input
    output_path = args.output
    name = args.name + ".pptx"
    title = args.title
    model = args.model
    debug = args.debug
    
    if debug:
        print(f"Input Path: {input_path}")
        print(f"Output Path: {output_path}")
        print(f"Presentation Name: {name}")
        print(f"Title: {title}")
        print(f"Model: {model}")
        print("Debug mode enabled.")
    
    # Step 1: Extract text from the input files
    extract(input_path)
    
    # Step 2: Generate flashcards from the extracted text
    file_paths = generate(input_path, output_path, model=model, debug=debug)
    
    # Step 3: Create a PowerPoint presentation from the generated flashcards
    if file_paths:
        create(output_path, name, file_paths, title)
    else:
        print("No flashcards generated.")
    
if __name__ == "__main__":
    main()
