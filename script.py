import os
import re
import csv
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            text = "\n".join(page.get_text("text") for page in doc)
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return text

def extract_text_from_image(image_path):
    """Extracts text from an image file using Tesseract OCR."""
    try:
        with Image.open(image_path) as img:
            return pytesseract.image_to_string(img)
    except Exception as e:
        print(f"Error reading image {image_path}: {e}")
        return ""

def find_pii(text):
    """Searches for PII in the given text using regex patterns."""
    
    patterns = {
    "Phone Number": r"\b\d{3}[-.]\d{3}[-.]\d{4}\b|\b\d{3}[-.]\d{4}\b",
    "Birthdate": r"\b(?:0[1-9]|1[0-2])[-/.](?:0[1-9]|[12][0-9]|3[01])[-/.](?:19|20)\d{2}\b",
    "Driver's License": r"\b(?:DL|Driver'?s License)(?:\s+\w+){0,4}\s*([A-Z0-9-]{6,10}\d[A-Z0-9-]*)\b(?![-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4})",  # Exclude phone numbers
    "Passport Number": r"\b(?:Passport Number|PPN)?(?:\s+\w+){0,4}\s*([A-Z0-9-]*\d[A-Z0-9-]*)\b(?=\b[A-Z0-9]{9}\b)",
    "Social Security Number": r"\b(?:SSN|Social Security Number)[:\s-]*(\d{3}[-\s]?\d{2}[-\s]?\d{4})\b",
    "Address": r"\b\d{1,5}\s[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Court|Ct|Way|Place|Pl),?\s*\b[A-Za-z\s]+,\s*[A-Za-z]{2}\s*\b\d{5}\b"
}

    matches = {category: list(set(re.findall(pattern, text, re.IGNORECASE))) for category, pattern in patterns.items() if re.findall(pattern, text, re.IGNORECASE)}
    
    # Only keep the first occurrence of each match
    for key in matches:
        matches[key] = matches[key][:1]

    return matches

def scan_folder(input_folder, output_csv):
    """Scans PDFs and image files in a folder for PII and saves results to a CSV."""
    results = []
    
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        text = ""
        
        if filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif filename.lower().endswith((".jpg", ".jpeg", ".png")):
            text = extract_text_from_image(file_path)
        
        if text:
            pii_matches = find_pii(text)
            for category, values in pii_matches.items():
                for match in values:
                    results.append([filename, f"{category}: {match}"])
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Document Name", "Detected PII Excerpt"])
        writer.writerows(results)

    print(f"Scan complete. Results saved to {output_csv}")

if __name__ == "__main__":
    scan_folder("A", "B/pii_report.csv")
