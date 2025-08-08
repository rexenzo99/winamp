#!/usr/bin/env python3
"""
Backend Test for 99 CENTS Car Stereo Player
This tests the static file serving and basic functionality
"""

import requests
import sys
from datetime import datetime

class CarStereoTester:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, test_func):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            success = test_func()
            if success:
                self.tests_passed += 1
                print(f"✅ Passed")
            else:
                print(f"❌ Failed")
            return success
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False

    def test_main_page_loads(self):
        """Test that the main HTML page loads correctly"""
        response = requests.get(self.base_url, timeout=10)
        if response.status_code != 200:
            print(f"Expected status 200, got {response.status_code}")
            return False
        
        content = response.text
        required_elements = [
            "99 CENTS Car Stereo Player",  # Title
            'class="deck"',                # Main deck element
            'id="playBtn"',               # Play button
            'id="nextBtn"',               # Next button
            'id="vol"',                   # Volume slider
            'id="ticker"',                # Ticker display
            'id="status"',                # Status display
            "alpine_faceplate.png"        # Background image
        ]
        
        for element in required_elements:
            if element not in content:
                print(f"Missing required element: {element}")
                return False
        
        print(f"Page size: {len(content)} bytes")
        return True

    def test_assets_load(self):
        """Test that required assets are accessible"""
        assets_to_test = [
            "/assets/alpine_faceplate.png",
            "/audio/track1.mp3",
            "/audio/track2.mp3", 
            "/audio/track3.mp3"
        ]
        
        all_passed = True
        for asset in assets_to_test:
            try:
                response = requests.head(f"{self.base_url}{asset}", timeout=5)
                if response.status_code == 200:
                    print(f"  ✅ {asset} - Available")
                else:
                    print(f"  ❌ {asset} - Status {response.status_code}")
                    all_passed = False
            except Exception as e:
                print(f"  ❌ {asset} - Error: {str(e)}")
                all_passed = False
        
        return all_passed

    def test_html_structure(self):
        """Test that HTML has proper structure for the car stereo"""
        response = requests.get(self.base_url, timeout=10)
        content = response.text
        
        # Check for essential JavaScript functionality
        js_checks = [
            "tracks = [",              # Playlist array
            "playPause()",            # Play/pause function
            "nextTrack()",            # Next track function
            "updateVolume()",         # Volume function
            "addEventListener",        # Event listeners
            "KeyD",                   # Debug mode key
            "Space",                  # Space key handler
            "ArrowRight",             # Arrow key handlers
        ]
        
        missing_js = []
        for check in js_checks:
            if check not in content:
                missing_js.append(check)
        
        if missing_js:
            print(f"Missing JavaScript functionality: {missing_js}")
            return False
        
        print("All essential JavaScript functionality present")
        return True

    def test_css_styling(self):
        """Test that CSS has proper styling for the car stereo"""
        response = requests.get(self.base_url, timeout=10)
        content = response.text
        
        css_checks = [
            ".deck {",                # Main deck styling
            ".btn",                   # Button styling
            ".slider",                # Slider styling
            ".ticker",                # Ticker styling
            ".debug",                 # Debug mode styling
            "@keyframes scroll",      # Scrolling animation
            "@media",                 # Responsive design
        ]
        
        missing_css = []
        for check in css_checks:
            if check not in content:
                missing_css.append(check)
        
        if missing_css:
            print(f"Missing CSS functionality: {missing_css}")
            return False
        
        print("All essential CSS styling present")
        return True

def main():
    print("🎵 99 CENTS CAR STEREO PLAYER - BACKEND TESTING")
    print("=" * 50)
    
    tester = CarStereoTester()
    
    # Run all tests
    tests = [
        ("Main Page Load", tester.test_main_page_loads),
        ("Assets Availability", tester.test_assets_load),
        ("HTML Structure", tester.test_html_structure),
        ("CSS Styling", tester.test_css_styling),
    ]
    
    for test_name, test_func in tests:
        tester.run_test(test_name, test_func)
    
    # Print results
    print(f"\n📊 BACKEND TEST RESULTS")
    print(f"Tests passed: {tester.tests_passed}/{tester.tests_run}")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 ALL BACKEND TESTS PASSED!")
        print("✅ Application is ready for frontend testing")
        return 0
    else:
        print("❌ Some backend tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())