from service import shorten_url
import logging

def main():
    # Configure logging to see errors and warnings
    logging.basicConfig(level=logging.INFO)
    
    test_url = "https://google.com"
    print(f"Shortening URL: {test_url}")
    
    short_code = shorten_url(test_url)
    
    if short_code:
        print(f"Success! Short code: {short_code}")
    else:
        print("Failed to shorten URL.")

if __name__ == "__main__":
    main()
