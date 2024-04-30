from .extract_text import extract_text
from .generate_flashcards import generate_flashcards
from .create_flashcards import create_flashcards
import shutil


def tearDown(dir):
    # empty and remove directory
    shutil.rmtree(dir)


def make_flashcards(input_path, output_path, output_name, title, prompt=None):
    # Extract text from PowerPoint files
    extracted_text = extract_text(input_path)

    # Generate flashcards using AI
    flashcard_data = generate_flashcards(prompt=prompt)

    # Create flashcards
    create_flashcards(output_path, output_name, title)

    # Clean up
    tearDown("./flashcard_data")
    tearDown("./extracted_data")


def make_flashcards_from_args(args):
    make_flashcards(args.input, args.output, args.name, args.title, prompt=args.prompt)
