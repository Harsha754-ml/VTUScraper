import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os

# URLs
BASE_URL = "https://results.vtu.ac.in/JJEcbcs25"
RESULT_URL = f"{BASE_URL}/index.php"

# Create session to manage cookies
session = requests.Session()

def get_captcha():
    """Fetch and display CAPTCHA image with error handling."""
    try:
        response = session.get(RESULT_URL, timeout=10)
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return False

    soup = BeautifulSoup(response.text, 'html.parser')
    captcha_img = soup.find('img', {'id': 'imgCaptcha'})

    if not captcha_img:
        print("❌ CAPTCHA not found.")
        return False

    captcha_url = f"{BASE_URL}/{captcha_img['src']}"
    try:
        captcha_img_response = session.get(captcha_url, timeout=10)
    except requests.RequestException as e:
        print(f"❌ Failed to retrieve CAPTCHA image: {e}")
        return False

    image = Image.open(BytesIO(captcha_img_response.content))
    image.save("captcha.jpg")
    os.startfile("captcha.jpg")
    return True

def fetch_result(usn, captcha):
    """Submit the form and parse result with error handling."""
    data = {
        'lns': usn,
        'captchacode': captcha,
        'submit': 'SUBMIT'
    }
    try:
        response = session.post(RESULT_URL, data=data, timeout=10)
    except requests.RequestException as e:
        print(f"❌ Network error during result fetch: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Error message?
    if "Invalid" in response.text or "not available" in response.text:
        print("❌ Invalid USN or CAPTCHA or result not available.")
        return

    # Parse result table
    table = soup.find("table", class_="table")
    if table:
        print("\n📄 RESULT")
        for row in table.find_all("tr"):
            columns = row.find_all(["th", "td"])
            print(" | ".join(col.get_text(strip=True) for col in columns))
    else:
        print("❌ Could not find result table.")

def main():
    usn = input("🎓 Enter USN (e.g., 1VA23CS001): ").strip().upper()
    if get_captcha():
        captcha = input("🔐 Enter CAPTCHA (check captcha.jpg): ").strip()
        fetch_result(usn, captcha)

if __name__ == "__main__":
    main()

# This script fetches the VTU results by handling CAPTCHA and USN input.
# Ensure you have the required libraries installed:
# pip install requests beautifulsoup4 pillow
# Note: The script assumes the VTU results page structure remains consistent.