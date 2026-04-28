from pypdf import PdfReader
import pandas as pd
import os

def parse_pdf(file_path: str):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def parse_csv(file_path: str):
    df = pd.read_csv(file_path)
    return df.to_string()


def parse_excel(file_path: str):
    df = pd.read_excel(file_path)
    return df.to_string()


def parse_file(file_path: str, file_type: str):
    if file_type == "pdf":
        return parse_pdf(file_path)
    
    elif file_type == "csv":
        return parse_csv(file_path)
    
    elif file_type == "xlsx":
        return parse_excel(file_path)
    
    else:
        raise ValueError("Unsupported file type")