#!/usr/bin/env python3
"""
Test script for VTU Result Scraper
"""

import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work correctly."""
    print("Testing imports...")
    
    try:
        import requests
        print("[OK] requests imported successfully")
    except ImportError as e:
        print(f"[FAIL] requests import failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("[OK] BeautifulSoup imported successfully")
    except ImportError as e:
        print(f"[FAIL] BeautifulSoup import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("[OK] PIL.Image imported successfully")
    except ImportError as e:
        print(f"[FAIL] PIL.Image import failed: {e}")
        return False
    
    try:
        import pytesseract
        print("[OK] pytesseract imported successfully")
    except ImportError as e:
        print(f"[FAIL] pytesseract import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("[OK] numpy imported successfully")
    except ImportError as e:
        print(f"[FAIL] numpy import failed: {e}")
        return False
    
    try:
        import cv2
        print("[OK] cv2 imported successfully")
    except ImportError:
        print("[WARN] cv2 not available (this is expected if not installed)")
    
    return True

def test_vtu_module():
    """Test that the vtu module can be imported."""
    print("\nTesting VTU module...")
    
    try:
        import vtu
        print("[OK] vtu module imported successfully")
        
        # Test that the cv2 fallback is working
        if hasattr(vtu, 'cv2'):
            if vtu.cv2 is None:
                print("[OK] OpenCV fallback is working correctly")
            else:
                print("[OK] OpenCV is available")
        
        return True
    except Exception as e:
        print(f"[FAIL] vtu module import failed: {e}")
        return False

def test_captcha_preprocessing():
    """Test the CAPTCHA preprocessing function."""
    print("\nTesting CAPTCHA preprocessing...")
    
    try:
        from PIL import Image
        import numpy as np
        import vtu
        
        # Create a dummy image
        dummy_image = Image.new('RGB', (100, 50), color='white')
        
        # Test the preprocessing function
        processed = vtu.preprocess_captcha(dummy_image)
        
        if isinstance(processed, np.ndarray):
            print("[OK] CAPTCHA preprocessing works correctly")
            return True
        else:
            print("[FAIL] CAPTCHA preprocessing returned unexpected type")
            return False
            
    except Exception as e:
        print(f"✗ CAPTCHA preprocessing test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("VTU Result Scraper - Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_vtu_module,
        test_captcha_preprocessing,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] All tests passed! The VTU Result Scraper is working correctly.")
        return True
    else:
        print("[FAILURE] Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)