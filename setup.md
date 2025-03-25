# Setup Instructions for PII Detection Script

This document provides setup instructions for running the **PII Detection Script** on both macOS and Windows. The script scans PDF and image files in a folder, detects sensitive PII data, and outputs the results into a CSV file.

## Prerequisites

- Python 3.6 or higher is required.
- The following libraries must be installed:
  - `PyMuPDF` for PDF text extraction
  - `pytesseract` for OCR-based text extraction from images
  - `Pillow` for image handling

## Setup Instructions

### 1. Install Tesseract OCR

#### macOS
If you're on macOS, you can install Tesseract using Homebrew:

```bash
brew install tesseract
```

For Windows:

Download the Tesseract installer from here (choose the latest version).

Run the installer and make sure to add Tesseract to the system PATH during installation (check the box for "Add Tesseract to PATH").

2. Create a Virtual Environment

macOS & Windows

Navigate to the project directory where script.py is located, then create a virtual environment:

bash

python -m venv .venv

3. Activate the Virtual Environment
macOS
To activate the virtual environment, run the following command:

bash

source .venv/bin/activate

Windows
To activate the virtual environment on Windows, run:

bash

source .venv/Scripts/activate

4. Install Required Python Libraries
With the virtual environment activated, install the necessary libraries using pip:

bash

pip install PyMuPDF pytesseract Pillow

5. Verify Tesseract Installation
Ensure that Tesseract is installed properly by running the following command:

bash

export PATH=$PATH:"/c/Users/aweymouth/Documents/Tesseract-OCR"

tesseract --version

This should display the version of Tesseract that was installed. If you see an error, ensure that Tesseract is properly installed and added to your PATH.

6. Run the Script

After setting up the virtual environment and installing the dependencies, run the script by executing:

bash

python script.py

The script will scan all PDF and image files in the A folder for PII and save the results to B/pii_report.csv.