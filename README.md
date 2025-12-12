# VTU Result Scraper

A Python script to fetch student results from the Visvesvaraya Technological University (VTU) website.

## Description

This script automates the process of fetching semester results from the official VTU results portal. It handles CAPTCHA by downloading the image and prompting the user to enter the text.

## Prerequisites

- Python 3.x
- The following Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `Pillow`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd vtu-result-scraper
   ```
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script from your terminal:
   ```bash
   python vtu.py
   ```
2. Choose an option:
   - **Option 1**: Single USN (for your own result)
   - **Option 2**: Multiple USNs (for fetching results for friends)
3. For single USN:
   - Enter your University Seat Number (USN) when prompted.
   - An image file named `captcha.jpg` will be created and opened. Enter the CAPTCHA text from the image.
   - The script will then fetch and display your results.
4. For multiple USNs:
   - Enter multiple USNs separated by commas (e.g., `1VA23CS001,1VA23CS002,1VA23CS003`)
   - An image file named `captcha.jpg` will be created and opened. Enter the CAPTCHA text from the image.
   - The script will fetch and display results for all USNs with a summary at the end.

## How It Works

The script sends a GET request to the VTU results page to obtain a session cookie and the CAPTCHA image. It then saves the CAPTCHA image locally and opens it for you to read. After you enter the USN and CAPTCHA, it sends a POST request to submit the form and retrieves the results. The HTML response is parsed using BeautifulSoup to extract and display the result table.

## Disclaimer

This script's functionality is dependent on the structure of the VTU results website. Any changes to the website's HTML structure or CAPTCHA implementation may break the script.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
