import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from datetime import datetime
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TDRC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class NewsToAudio:
    def __init__(self, output_dir='./audio_output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def fetch_bloomberg_content(self, url):
        """Special handler for Bloomberg articles using Selenium"""
        if '.com/' in url and '.com./' not in url:
            url = url.replace('.com/', '.com./')
        
        print("Setting up Chrome options...")
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Updated headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")  # Added for headless mode
        chrome_options.add_argument("--disable-extensions")  # Disable extensions
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        driver = None
        try:
            print("Installing Chrome driver...")
            service = Service(ChromeDriverManager(version="latest").install())
            
            print("Initializing Chrome driver...")
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            print("Setting up browser properties...")
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """
            })
            
            print(f"Fetching URL: {url}")
            driver.get(url)
            
            print("Waiting for page load...")
            wait = WebDriverWait(driver, 30)
            
            # More specific selectors for Bloomberg graphics articles
            selectors = [
                "article",
                ".article-body",
                ".body-content",
                ".story-body",
                ".graphics-article",
                ".graphics-content",
                ".article-content"
            ]
            
            # Wait for any of these selectors
            for selector in selectors:
                try:
                    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    print(f"Found content using selector: {selector}")
                    break
                except:
                    continue
            
            # Scroll through the page to load lazy content
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(3)
            
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Save debug info
            with open('debug_response.html', 'w', encoding='utf-8') as f:
                f.write(page_source)
            
            # Try to find title with more specific selectors
            title = None
            title_selectors = [
                ('h1', {'class': 'headline'}),
                ('h1', {'class': 'article-title'}),
                ('h1', {'class': 'graphics-title'}),
                ('div', {'class': 'headline'}),
                ('meta', {'property': 'og:title'}),
                ('h1', {})
            ]
            
            for tag, attrs in title_selectors:
                element = soup.find(tag, attrs)
                if element:
                    title = element.get('content') if tag == 'meta' else element.get_text().strip()
                    if title:
                        print(f"Found title using {tag}: {title}")
                        break
            
            # Try to find content with more specific selectors
            content_parts = []
            content_selectors = [
                ('div', {'class': 'body-content'}),
                ('div', {'class': 'graphics-article'}),
                ('div', {'class': 'article-body'}),
                ('div', {'class': 'story-body'}),
                ('article', {}),
            ]
            
            for tag, attrs in content_selectors:
                element = soup.find(tag, attrs)
                if element:
                    paragraphs = element.find_all(['p', 'h2', 'h3', 'li'])
                    text = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                    if text:
                        content_parts.append(text)
            
            content = '\n\n'.join(content_parts)
            
            if not title:
                title = "Untitled Bloomberg Article"
                print("Warning: Could not find article title")
            
            if not content:
                print("Warning: Using fallback content extraction method")
                paragraphs = soup.find_all('p')
                content = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            
            if not content:
                raise ValueError("Could not extract article content")
            
            print(f"\nExtracted content length: {len(content)} characters")
            return title, content
            
        except Exception as e:
            print(f"Error details: {str(e)}")
            raise
            
        finally:
            try:
                driver.quit()
            except:
                pass

    def create_audio(self, title, content):
        """Create MP3 with metadata for Apple Music"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{self._sanitize_filename(title)}.mp3"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create MP3 using gTTS
        tts = gTTS(text=f"{title}. {content}", lang='en')
        tts.save(filepath)
        
        # Add ID3 tags for better Apple Music integration
        try:
            audio = ID3(filepath)
        except:
            audio = ID3()
        
        audio.add(TIT2(encoding=3, text=title))  # Title
        audio.add(TPE1(encoding=3, text="News Reader"))  # Artist
        audio.add(TALB(encoding=3, text="Bloomberg Articles"))  # Album
        audio.add(TCON(encoding=3, text="News"))  # Genre
        audio.add(TDRC(encoding=3, text=str(datetime.now().year)))  # Year
        
        audio.save(filepath)
        return filepath

    def _sanitize_filename(self, filename):
        return "".join(x for x in filename if x.isalnum() or x in (' ', '-', '_')).strip()

    def process_article(self, url):
        """Main method to convert article to audio"""
        try:
            title, content = self.fetch_bloomberg_content(url)
            print(f"\n=== Article Content ===")
            print(f"Title: {title}")
            print(f"\nFirst 1000 characters of content:")
            print(f"{content[:1000]}...")
            print("\n=== End of Preview ===\n")
            
            audio_path = self.create_audio(title, content)
            print(f"Created MP3 file at: {audio_path}")
            print("\nYou can now import this MP3 file into Apple Music!")
            
            return audio_path
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return None 

    def fetch_news_api_content(self, query):
        """Fetch news using NewsAPI instead of direct scraping"""
        API_KEY = 'your_newsapi_key'  # Get from newsapi.org
        url = f'https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}'
        
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'ok' and data['articles']:
            article = data['articles'][0]  # Get first matching article
            title = article['title']
            content = f"{article['description']}\n\n{article['content']}"
            return title, content
        else:
            raise Exception("No articles found") 