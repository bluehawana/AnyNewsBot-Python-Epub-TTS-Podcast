import requests
from bs4 import BeautifulSoup
import pyttsx3
from datetime import datetime
import os
from gtts import gTTS
import feedgenerator
import yaml

class NewsToAudio:
    def __init__(self, config_path='config.yml'):
        # Load configuration
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.output_dir = self.config['output_directory']
        self.feed_dir = os.path.join(self.output_dir, 'feed')
        os.makedirs(self.feed_dir, exist_ok=True)

    def fetch_bloomberg_content(self, url):
        """Special handler for Bloomberg articles using the dot trick"""
        # Insert dot after .com if not present
        if '.com/' in url and '.com./' not in url:
            url = url.replace('.com/', '.com./')
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise exception for bad status codes
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the title - Bloomberg usually has it in a specific h1 tag
            title = soup.find('h1')
            title = title.get_text().strip() if title else "Untitled Bloomberg Article"
            
            # For Bloomberg articles, we want to get all paragraph text
            paragraphs = soup.find_all('p')
            content = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            
            if not content:
                raise ValueError("Could not extract article content")
            
            return title, content
            
        except Exception as e:
            raise Exception(f"Error fetching Bloomberg article: {str(e)}")

    def fetch_content(self, url):
        """Main content fetching method"""
        if 'bloomberg.com' in url:
            return self.fetch_bloomberg_content(url)
        
        # Original fetch logic for other sites
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        article = soup.find("article")
        if not article:
            raise ValueError("Could not find article content")
        
        title = soup.title.string
        content = article.get_text(separator=' ', strip=True)
        
        return title, content

    def create_audio(self, title, content):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{self._sanitize_filename(title)}.mp3"
        filepath = os.path.join(self.feed_dir, filename)
        
        # Use gTTS instead of pyttsx3 for better quality
        tts = gTTS(text=f"{title}. {content}", lang='en')
        tts.save(filepath)
        
        return filepath

    def update_podcast_feed(self, title, audio_path):
        feed = feedgenerator.Rss201rev2Feed(
            title="My News Podcast",
            link=self.config['podcast_url'],
            description="Automated news articles converted to audio",
            language="en"
        )

        # Add the new item to the feed
        feed.add_item(
            title=title,
            link=f"{self.config['podcast_url']}/{os.path.basename(audio_path)}",
            enclosure=audio_path,
            pubdate=datetime.now(),
            description=title
        )

        # Write the RSS feed
        with open(os.path.join(self.output_dir, 'podcast.xml'), 'w') as fp:
            feed.write(fp, 'utf-8')

    def _sanitize_filename(self, filename):
        return "".join(x for x in filename if x.isalnum() or x in (' ', '-', '_')).strip()

    def process_article(self, url):
        try:
            title, content = self.fetch_content(url)
            audio_path = self.create_audio(title, content)
            self.update_podcast_feed(title, audio_path)
            return True
        except Exception as e:
            print(f"Error processing article: {str(e)}")
            return False 