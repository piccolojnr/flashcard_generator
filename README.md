# Flashcard Generator

## Overview

The Flashcard Generator is a unified tool designed to extract text from various file formats (such as `.pptx`, `.pdf`, `.txt`, `.docx`), generate flashcards using an AI model, and create a PowerPoint presentation from those flashcards.

## Features

- **Text Extraction**: Extract text from supported file types.
- **Flashcard Generation**: Generate flashcards with questions and answers using an AI model.
- **PowerPoint Creation**: Create a PowerPoint presentation from the generated flashcards.
- **Caching**: Cache the flashcards to improve performance on subsequent runs.

## Requirements

- Python 3.6+
- `argparse`
- `os`
- `json`
- `tqdm`
- `requests`
- `python-pptx`
- `random`
- [Ollama](https://ollama.com/) installed and configured with a working model pulled

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/piccolojnr/flashcard-generator.git
   ```

2. Change into the project directory:

   ```sh
   cd flashcard-generator
   ```

3. Install the required Python packages:

   ```sh
   pip install -r requirements.txt
   ```
4. Install [Ollama](https://ollama.com/) and ensure you have a working model pulled:

   Follow the instructions on the [Ollama website](https://ollama.com/docs/installation) to install Ollama and pull the required model.

## Usage

The main script is `flashcard_generator.py`, which can be run from the command line. Here are the available options:

- `-i`, `--input`: Path to the input file or directory containing supported files.
- `-o`, `--output`: Path to the output directory.
- `-n`, `--name`: Name of the output PowerPoint presentation file (without extension).
- `-t`, `--title`: Title of the output presentation.
- `-m`, `--model`: Specify the AI model to use (default is `llama3`).
- `-d`, `--debug`: Enable debug mode.

### Example Command

```sh
./flashcard_generator.py -i ./input_files -o ./output_files -n flashcards_presentation -t "My Flashcards" -m llama3 -d
```

## Project Structure

```
flashcard-generator/
├── README.md
├── requirements.txt
├── flashcard_generator.py
├── scripts/
│   ├── extract_text.py
│   ├── generate_flashcards.py
│   ├── create_presentation.py
├── static/
│   ├── conf.json
│   └── template_files/  # any template images or fonts
├── input_files/  # example input files
├── output_files/  # generated output files
└── cache/  # cache for storing flashcards
```

## Configuration

The `static/conf.json` file contains configuration details for the PowerPoint presentation, such as layout, text styles, and images for the slides.

## Functionality

### Extracting Text

The `extract_text.py` script handles extracting text from input files. It supports `.pptx`, `.pdf`, `.txt`, and `.docx` file formats.

### Generating Flashcards

The `generate_flashcards.py` script uses an AI model to generate flashcards from the extracted text. It stores the flashcards in a cache to avoid redundant computations.

### Creating the Presentation

The `create_presentation.py` script generates a PowerPoint presentation from the flashcards using the configurations specified in `static/conf.json`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- [python-pptx](https://github.com/scanny/python-pptx) for PowerPoint file generation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for any bugs or feature requests.
