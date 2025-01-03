from news_to_audio import NewsToAudio

def test_bloomberg_article():
    converter = NewsToAudio()
    
    # Use the specific graphics article URL
    url = "https://www.bloomberg.com./graphics/2025-investment-outlooks/?embedded-checkout=true"
    
    try:
        audio_path = converter.process_article(url)
        if audio_path:
            print("\nSuccess! Next steps:")
            print("1. Find the MP3 file at:", audio_path)
            print("2. Import the file into Apple Music")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_bloomberg_article() 