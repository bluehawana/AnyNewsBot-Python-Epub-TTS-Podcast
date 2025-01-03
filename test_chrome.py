from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def test_chrome_setup():
    print("1. Testing Chrome setup...")
    
    try:
        print("2. Setting up Chrome options...")
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        print("3. Installing Chrome driver...")
        service = Service(ChromeDriverManager(version="latest").install())
        
        print("4. Initializing Chrome driver...")
        driver = webdriver.Chrome(service=service, options=options)
        
        print("5. Testing simple page load...")
        driver.get("https://www.google.com")
        
        print("6. Chrome setup successful!")
        return True
        
    except Exception as e:
        print(f"Error setting up Chrome: {str(e)}")
        return False
        
    finally:
        if 'driver' in locals():
            print("7. Closing Chrome...")
            driver.quit()

if __name__ == "__main__":
    test_chrome_setup() 