# NewsBot - Bloomberg Article to Audio Converter

A Python tool that converts Bloomberg articles to audio files using the "dot trick". Perfect for listening to financial news during commutes or workouts.

## 🌟 Key Features
- Bypasses Bloomberg's paywall using the "dot trick"
- Converts articles to high-quality MP3 files
- Adds proper metadata for Apple Music
- Uses advanced web scraping techniques
- Easy to use and customize

## 📋 Prerequisites
- Python 3.x
- Google Chrome browser
- macOS/Linux/Windows

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/bluehawana/AnyNewsBot-Python-Epub-TTS-Podcast.git
cd NewsBot
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📝 File Descriptions

### news_to_audio.py
Main class that handles article fetching and conversion to audio.

```python
class NewsToAudio:
    def __init__(self, output_dir='./audio_output'):
        # Initialization code here

    def fetch_bloomberg_content(self, url):
        # Fetch article content

    def create_audio(self, title, content):
        # Convert content to audio

    def process_article(self, url):
        # Process the article URL
```

### Other Files
- `test_article.py`: Tests article conversion with Bloomberg URLs
- `test_chrome.py`: Verifies Chrome and Selenium setup
- `example_usage.py`: Usage examples for the tool
- `audio_output/`: Directory for generated MP3 files

## 🔧 Troubleshooting

### Chrome Driver Issues:
- Ensure that the Chrome driver is installed and in the PATH

### Article Access Issues:
- Make sure the URL contains the dot after .com
- Example: www.bloomberg.com./news/articles/...

### Audio Output Issues:
- Check audio_output directory permissions
- Verify Chrome installation

## Known Issues
- Some articles may require additional authentication
- Audio quality depends on gTTS settings
- Chrome updates may require driver updates

## 🔮 Future Improvements
- Support for other news sources
- Custom voice options
- Batch processing
- GUI interface
- API integration

## 📄 License
MIT License - See LICENSE file for details.

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## 📧 Contact
Create an issue in the repository for questions or suggestions.

## Disclaimer
This tool is for educational purposes only. Please respect Bloomberg's terms of service and copyright policies.

---

Remember to star ⭐ the repository if you find it helpful!