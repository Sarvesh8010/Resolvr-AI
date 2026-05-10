from pypdf import PdfReader

import pandas as pd

import pytesseract

from pdf2image import convert_from_path

from PIL import Image


# ---------------- PDF PARSER ----------------

def parse_pdf(file_path: str):

    reader = PdfReader(file_path)

    text = ""

    # NORMAL PDF TEXT EXTRACTION
    for page in reader.pages:

        text += page.extract_text() or ""

    # OCR FALLBACK
    if text.strip() == "":
    
        print("Running OCR on scanned PDF...")
    
        images = convert_from_path(
            file_path,
            poppler_path=r"C:\poppler\poppler-26.02.0\Library\bin"
        )
    
        for image in images:
        
            text += pytesseract.image_to_string(
                image
            )

    return text


# ---------------- CSV PARSER ----------------

def parse_csv(file_path: str):

    df = pd.read_csv(file_path)

    return df.to_string()


# ---------------- EXCEL PARSER ----------------

def parse_excel(file_path: str):

    df = pd.read_excel(file_path)

    return df.to_string()


# ---------------- IMAGE OCR ----------------

def parse_image(file_path: str):

    image = Image.open(file_path)

    text = pytesseract.image_to_string(
        image
    )

    return text


# ---------------- MAIN PARSER ----------------

def parse_file(
    file_path: str,
    file_type: str
):

    if file_type == "pdf":

        return parse_pdf(file_path)

    elif file_type == "csv":

        return parse_csv(file_path)

    elif file_type == "xlsx":

        return parse_excel(file_path)

    elif file_type in [
        "png",
        "jpg",
        "jpeg"
    ]:

        return parse_image(file_path)

    else:

        raise ValueError(
            "Unsupported file type"
        )