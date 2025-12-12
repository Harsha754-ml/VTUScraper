import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os
import pytesseract
import numpy as np
import re

try:
    import cv2
except ImportError:
    cv2 = None
    print("Warning: OpenCV (cv2) not installed. Auto CAPTCHA solving will use basic image processing.")

# Main VTU page
VTU_URL = "https://results.vtu.ac.in/"

# Create session to manage cookies
session = requests.Session()
# Disable SSL verification due to VTU certificate issues
session.verify = False

def get_latest_result_url():
    """Fetches the latest result URL from the main VTU page."""
    print(f"Fetching latest result URL from {VTU_URL}...")
    try:
        response = session.get(VTU_URL, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the link that contains "cbcs" and "result" case-insensitively
        result_link = soup.find(
            'a', 
            href=re.compile(r"vtu.ac.in/.*[cC][bB][cC][sS].*"),
            string=re.compile(r'click here for.* cbcs.* results', re.IGNORECASE)
        )
        
        if result_link and result_link.has_attr('href'):
            url = result_link['href']
            print(f"Found result link: {url}")
            return url.rstrip('/')
        
        # Fallback if the specific text isn't found
        print("Primary link not found, trying fallback...")
        result_link = soup.find('a', href=re.compile(r"results.vtu.ac.in/.*[cC][bB][cC][sS].*"))
        if result_link and result_link.has_attr('href'):
            url = result_link['href']
            print(f"Found fallback result link: {url}")
            return url.rstrip('/')

    except requests.RequestException as e:
        print(f"Network error while fetching the main result page: {e}")
    
    print("Could not automatically determine the result URL.")
    return None

# URLs - only set these when running directly, not when importing
if __name__ == "__main__":
    BASE_URL = get_latest_result_url()
    if not BASE_URL:
        # Ask user to input the URL manually as a last resort
        BASE_URL = input("Please manually enter the full result URL (e.g., https://results.vtu.ac.in/JJEcbcs25): ").strip()
        if not BASE_URL:
            print("No result URL provided. Exiting.")
            exit()

    RESULT_URL = f"{BASE_URL}/index.php"
else:
    # When importing, use dummy values to avoid input prompts
    BASE_URL = "https://results.vtu.ac.in/dummy"
    RESULT_URL = f"{BASE_URL}/index.php"

def preprocess_captcha(image):
    """Preprocess CAPTCHA image for better OCR results."""
    img_array = np.array(image.convert('RGB'))
    
    if cv2 is not None:
        # Use OpenCV for advanced processing
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        
        # Adaptive thresholding can be more robust
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Invert colors so text is black on white background
        thresh = cv2.bitwise_not(thresh)
        
        # Remove noise
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        return processed
    else:
        # Basic preprocessing without OpenCV
        # Convert to grayscale manually
        gray = np.dot(img_array[...,:3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
        
        # Simple thresholding
        thresh = (gray > 128).astype(np.uint8) * 255
        
        # Invert colors
        thresh = 255 - thresh
        
        return thresh

def solve_captcha_automatically(image):
    """Attempt to solve CAPTCHA using OCR."""
    try:
        processed_img = preprocess_captcha(image)
        
        captcha_text = pytesseract.image_to_string(
            processed_img,
            config='--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        ).strip()
        
        captcha_text = ''.join(filter(str.isalnum, captcha_text)) # Keep only alphanumeric
        
        if len(captcha_text) == 6: # Basic validation
            print(f"Auto-detected CAPTCHA: {captcha_text}")
            return captcha_text
        else:
            print(f"Auto-detected text '{captcha_text}' is not a valid CAPTCHA. Retrying may work.")
            return None
        
    except Exception as e:
        print(f"Auto CAPTCHA solving failed: {e}")
        return None

def get_captcha(auto_solve=False):
    """Fetch and display CAPTCHA image with error handling."""
    try:
        response = session.get(RESULT_URL, timeout=10)
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return False, None

    soup = BeautifulSoup(response.text, 'html.parser')
    captcha_img = soup.find('img', {'alt': 'CAPTCHA code'}) or soup.find('img', {'id': 'imgCaptcha'})

    if not captcha_img:
        print("CAPTCHA image not found. The VTU website structure may have changed.")
        return False, None

    captcha_src = captcha_img['src']
    # Construct absolute URL for the CAPTCHA image
    captcha_url = f"{BASE_URL}/{captcha_src.lstrip('/')}"
    
    try:
        captcha_img_response = session.get(captcha_url, timeout=10)
    except requests.RequestException as e:
        print(f"Failed to retrieve CAPTCHA image: {e}")
        return False, None

    image = Image.open(BytesIO(captcha_img_response.content))
    
    if auto_solve:
        captcha_text = solve_captcha_automatically(image)
        if captcha_text:
            return True, captcha_text
    
    # Fallback to manual if auto-solve is off or fails
    try:
        image.save("captcha.jpg")
        os.startfile("captcha.jpg")
        print("Check captcha.jpg for the image.")
    except Exception as e:
        print(f"Could not open captcha image: {e}")

    return True, None

def fetch_result(usn, captcha):
    """Submit the form and parse result with error handling."""
    data = {'lns': usn, 'captchacode': captcha, 'submit': 'SUBMIT'}
    try:
        response = session.post(RESULT_URL, data=data, timeout=10)
    except requests.RequestException as e:
        print(f"Network error during result fetch for {usn}: {e}")
        return False

    soup = BeautifulSoup(response.text, 'html.parser')

    if "Invalid" in response.text or "not available" in response.text:
        print(f"Invalid USN or CAPTCHA or result not available for {usn}.")
        return False

    table = soup.find("table", class_="table")
    if table:
        print(f"\nRESULT FOR {usn}")
        for row in table.find_all("tr"):
            columns = row.find_all(["th", "td"])
            print(" | ".join(col.get_text(strip=True) for col in columns))
        return True
    else:
        print(f"Could not find result table for {usn}. The website may have changed.")
        return False

def process_usns(usns, auto_solve=False):
    """Process a list of USNs with a single CAPTCHA."""
    if not usns:
        print("No valid USNs provided.")
        return
    
    print(f"Processing {len(usns)} USN(s): {', '.join(usns)}")
    
    success, captcha = get_captcha(auto_solve=auto_solve)
    if not success:
        return

    if not captcha:
        captcha = input("Enter CAPTCHA from captcha.jpg: ").strip()
    
    successful_results = 0
    for usn in usns:
        print(f"\nFetching result for {usn}...")
        if fetch_result(usn, captcha):
            successful_results += 1
        print("-" * 50)
    
    print(f"\nSummary: {successful_results}/{len(usns)} results fetched successfully.")


def main():
    """Main function to drive the scraper."""
    print("VTU Result Scraper")
    print("WARNING: SSL verification disabled due to VTU certificate issues")
    print("-" * 30)
    print("1. Single USN")
    print("2. Multiple USNs")
    print("3. Single USN (Auto CAPTCHA)")
    print("4. Multiple USNs (Auto CAPTCHA)")
    choice = input("Choose option (1/2/3/4): ").strip()
    
    auto_solve = choice in ['3', '4']
    multiple_usns = choice in ['2', '4']

    if multiple_usns:
        usns_input = input("Enter USNs separated by commas: ").strip()
        usns = [usn.strip().upper() for usn in usns_input.split(',') if usn.strip()]
    else:
        usn = input("Enter a single USN: ").strip().upper()
        usns = [usn] if usn else []

    process_usns(usns, auto_solve)

if __name__ == "__main__":
    main()

# This script fetches the VTU results by handling CAPTCHA and USN input.
# Ensure you have the required libraries installed: pip install -r requirements.txt
# WARNING: SSL verification is disabled due to VTU certificate issues.
# This is not recommended for production but necessary for VTU's current setup.