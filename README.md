### Project Documentation

#### Introduction
This project is a toolset designed to facilitate various operations related to extracting, generating, and managing flashcards. The toolset comprises several scripts, each serving a specific purpose, such as extracting text from documents, generating flashcards from JSON data, creating flashcards from AI-generated content, extracting JSON data from HTML files, and generating flashcards from PowerPoint files.

#### Usage
The project is implemented in Python and utilizes command-line arguments for operation. Below are the main functionalities provided by the project along with their respective command-line usage:

1. **Extract Text (`extract` command)**
   - Description: Extracts text from supported document formats.
   - Command: `./project.py extract -i <input_path> -o <output_path> [-cl <character_limit>]`
     - `-i, --input`: Path to the input file or folder (.pptx, .pdf, .txt, .docx).
     - `-o, --output`: Path to the output file or folder.
     - `-cl, --character-limit`: Optional. Character limit for each output file.

2. **Generate Flashcards (`generate-flashcards` command)**
   - Description: Generates flashcards presentation from JSON file(s).
   - Command: `./project.py generate-flashcards -i <input_path> -o <output_name> -t <title> [-c <config>]`
     - `-i, --input`: Path to the JSON file or directory containing JSON files.
     - `-o, --output`: Name of the output PowerPoint presentation file (without extension).
     - `-t, --title`: Title of the output presentation.
     - `-c, --config`: Optional. Path to the configuration file (default: static/conf.json).

3. **Extract JSON (`extract-json` command)**
   - Description: Extracts JSON data from HTML content.
   - Command: `./project.py extract-json -i <input_path> -o <output_path> [-m] [-l <limit>]`
     - `-i, --input`: Path to the HTML file or folder.
     - `-o, --output`: Path to the output file (json) or folder (no extension).
     - `-m, --merge`: Optional. Merge all extracted data into a single file.
     - `-l, --limit`: Optional. List length for the output file.

4. **Generate Flashcards from AI (`generate-flashcards-from-ai` command)**
   - Description: Generates flashcards from AI-generated content.
   - Command: `./project.py generate-flashcards-from-ai -i <input_path> -o <output_path>`
     - `-i, --input`: Path to the text file or folder (txt).
     - `-o, --output`: Path to the output folder.

5. **Make Flashcards (`make-flashcards` command)**
   - Description: Generates flashcards from PowerPoint files.
   - Command: `./project.py make-flashcards -i <input_path> -o <output_path> -n <name> -t <title> [-p <prompt>]`
     - `-i, --input`: Path to the file or directory containing the files (.pptx, .pdf, .txt, .docx).
     - `-o, --output`: Path to the output directory.
     - `-n, --name`: Name of the output PowerPoint presentation file (without extension).
     - `-t, --title`: Title of the output presentation.
     - `-p, --prompt`: Optional. Prompt to use for the AI model. If not specified, the default prompt will be used.

#### How to Run
To execute any of the functionalities provided by the project, follow these steps:
1. Open a terminal.
2. Navigate to the project directory.
3. Run the desired command using the specified format and arguments.

#### Dependencies
The project relies on the following dependencies:
- Python 3.x
- argparse (for command-line argument parsing)

