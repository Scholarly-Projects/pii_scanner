import os
import re
import csv
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def extract_text_from_image(image_path):
    """Extract text from an image file using Tesseract OCR."""
    try:
        img = Image.open(image_path)
        return pytesseract.image_to_string(img)
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
        return ""

def find_pii(text):
    """Search for PII in the given text."""
    patterns = {
        "Full Name": r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b",
        "Phone Number": r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "Birthdate": r"\b\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}\b",
        "Driver's License": r"\b[A-Z0-9]{6,10}\b",
        "Passport Number": r"\b[A-Z0-9]{6,9}\b",
        "Employee ID": r"\b[0-9]{5,10}\b"
    }
    matches = {}
    for category, pattern in patterns.items():
        found = re.findall(pattern, text)
        if found:
            matches[category] = found
    return matches

def scan_folder(input_folder, output_csv):
    """Scan all PDFs and JPGs in a folder for PII and save results to CSV."""
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
