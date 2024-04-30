from pptx import Presentation
import os
from pypdf import PdfReader

import docx2txt


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
        for i in range(0, len(page.extract_text()), cl):
            extracted_text.append(page.extract_text()[i : i + cl])

    return "\n".join(extracted_text)


def extract_text_from_pptx(pptx_file_path, cl):
    presentation = Presentation(pptx_file_path)
    extracted_text = []

    for slide in presentation.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text
                for i in range(0, len(text), cl):
                    extracted_text.append(text[i : i + cl])
                extracted_text.append(text)

    return "\n".join(extracted_text)


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
