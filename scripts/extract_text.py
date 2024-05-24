from pptx import Presentation
import os
from pypdf import PdfReader

import docx2txt

import re


# Function to clean up extracted text
def clean_text(text):
    # Remove extra spaces and line breaks
    text = re.sub(r"\s+", " ", text)
    # Remove special characters
    text = re.sub(r"[^A-Za-z0-9\s]", "", text)
    return text.strip()


# Function to process extracted text


def process_text(extracted_text, character_limit):
    cleaned_text_chunks = []
    for text in extracted_text:
        cleaned_text = clean_text(text)
        chunks = [
            cleaned_text[i : i + character_limit]
            for i in range(0, len(cleaned_text), character_limit)
        ]
        cleaned_text_chunks.extend(chunks)
    return cleaned_text_chunks


def extract_text_from_txt(txt_file_path, cl):
    extracted_text = []
    with open(txt_file_path, "r") as file:
        text = file.read()
        for i in range(0, len(text), cl):
            extracted_text.append(text[i : i + cl])

    return "\n".join(extracted_text)


def extract_text_from_docx(docx_file_path, cl):
    extracted_text = []

    text = docx2txt.process(docx_file_path)
    for i in range(0, len(text), cl):
        extracted_text.append(text[i : i + cl])

    return "\n".join(extracted_text)


def extract_text_from_pdf(pdf_file, cl):
    extracted_text = []

    reader = PdfReader(pdf_file)

    for page in reader.pages:
        extracted_text.append(page.extract_text())

    return extracted_text


def extract_text_from_pptx(pptx_file_path, cl):
    presentation = Presentation(pptx_file_path)
    extracted_text = []

    for slide in presentation.slides:
        slide_text = ""
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text.strip()
                slide_text += text + "\n"
        extracted_text.append(slide_text)

    return extracted_text


def process_pptx_files(input_path, output_path, character_limit):
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)
    extracted_data = []

    if os.path.isfile(input_path):
        if input_path.endswith(".pptx"):
            extracted_data.extend(extract_text_from_pptx(input_path, character_limit))
        elif input_path.endswith(".pdf"):
            extracted_data.extend(extract_text_from_pdf(input_path, character_limit))
        elif input_path.endswith(".txt"):
            extracted_data.extend(extract_text_from_txt(input_path, character_limit))
        elif input_path.endswith(".docx"):
            extracted_data.append(extract_text_from_docx(input_path, character_limit))
    elif os.path.isdir(input_path):
        for file in os.listdir(input_path):
            if file.endswith(".pptx"):
                extracted_data.append(
                    extract_text_from_pptx(
                        os.path.join(input_path, file), character_limit
                    )
                )
            elif file.endswith(".pdf"):
                extracted_data.extend(
                    extract_text_from_pdf(
                        os.path.join(input_path, file), character_limit
                    )
                )
            elif file.endswith(".txt"):
                extracted_data.extend(
                    extract_text_from_txt(
                        os.path.join(input_path, file), character_limit
                    )
                )
            elif file.endswith(".docx"):
                extracted_data.append(
                    extract_text_from_docx(
                        os.path.join(input_path, file), character_limit
                    )
                )
    else:
        print("Invalid input path.")
        return

    extracted_data = process_text(extracted_data, character_limit)

    if os.path.exists(output_path) and os.listdir(output_path):
        raise ValueError("Output path is not empty.")
    elif not os.path.exists(output_path):
        os.makedirs(output_path)

    buffer = ""
    file_count = 0
    for data in extracted_data:
        if character_limit and len(buffer + data) > character_limit:
            with open(
                os.path.join(output_path, f"output_{file_count}.txt"),
                "w",
                encoding="utf-8",
            ) as output_file:
                output_file.write(buffer)
            buffer = ""
            file_count += 1
        buffer += data

    if buffer:
        with open(
            os.path.join(output_path, f"output_{file_count+1}.txt"), "w"
        ) as output_file:
            output_file.write(buffer)

    print(f"Output files saved to {output_path}.")


def extract_text_from_args(args):
    try:
        if not args.input:
            raise ValueError("Input path is required.")
        if not args.output:
            raise ValueError("Output path is required.")
        if not os.path.exists(args.input):
            raise ValueError("Input path does not exist.")

        print(args)
        process_pptx_files(args.input, args.output, args.character_limit)
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"Error: {e}")
        exit()


def extract_text(input_path):
    try:
        if not os.path.exists(input_path):
            raise ValueError("Input path does not exist.")

        process_pptx_files(input_path, "./extracted_data", 4000)
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"Error: {e}")
        exit()
