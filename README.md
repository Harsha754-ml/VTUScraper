# VTU Result Scraper

A Python script to fetch student results from the Visvesvaraya Technological University (VTU) website.

## Description

This script automates the process of fetching semester results from the official VTU results portal. It can handle CAPTCHA in two ways:
- **Manual mode**: Downloads the CAPTCHA image and prompts you to enter the text
- **Auto mode**: Attempts to automatically read the CAPTCHA using OCR (Optical Character Recognition)

**Note about SSL**: Due to certificate issues with the VTU website, SSL verification is disabled in this script. This may generate warnings but is necessary for the script to work with VTU's current setup.

**Note about Auto CAPTCHA**: The auto CAPTCHA feature uses OCR technology which may not always be 100% accurate. If it fails, the script will fall back to manual entry.

## Prerequisites

- Python 3.x
- The following Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `Pillow`
  - `pytesseract` (for auto CAPTCHA solving)
  - `opencv-python` (for image processing)
  - `numpy` (for image processing)
- Tesseract OCR installed on your system (for auto CAPTCHA solving)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Harsha754-ml/VTUScraper.git
   ```
2. Navigate to the project directory:
   ```bash
   cd vtu-result-scraper
   ```
3. Install Tesseract OCR (required for auto CAPTCHA solving):
   - **Windows**: Download installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Mac**: `brew install tesseract`
   - **Linux**: `sudo apt install tesseract-ocr`
4. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script from your terminal:
   ```bash
   python vtu.py
   ```
2. Choose an option:
   - **Option 1**: Single USN (for your own result) - Manual CAPTCHA entry
   - **Option 2**: Multiple USNs (for fetching results for friends) - Manual CAPTCHA entry
   - **Option 3**: Single USN with Auto CAPTCHA - Attempts to automatically solve CAPTCHA
   - **Option 4**: Multiple USNs with Auto CAPTCHA - Attempts to automatically solve CAPTCHA
3. For manual CAPTCHA options (1 & 2):
   - Enter your University Seat Number(s) when prompted.
   - An image file named `captcha.jpg` will be created and opened. Enter the CAPTCHA text from the image.
   - The script will then fetch and display your results.
4. For auto CAPTCHA options (3 & 4):
   - Enter your University Seat Number(s) when prompted.
   - The script will attempt to automatically read the CAPTCHA using OCR.
   - If auto-solving fails, it will fall back to manual entry.
   - The script will then fetch and display your results.

## How It Works

The script sends a GET request to the VTU results page to obtain a session cookie and the CAPTCHA image. It then saves the CAPTCHA image locally and opens it for you to read. After you enter the USN and CAPTCHA, it sends a POST request to submit the form and retrieves the results. The HTML response is parsed using BeautifulSoup to extract and display the result table.

## Disclaimer

This script's functionality is dependent on the structure of the VTU results website. Any changes to the website's HTML structure or CAPTCHA implementation may break the script.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
