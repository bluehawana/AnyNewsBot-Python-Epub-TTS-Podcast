from news_to_podcast import NewsToAudio
import ebooklib
from ebooklib import epub
import os

def test_bloomberg_article():
    converter = NewsToAudio()
    url = "https://www.bloomberg.com./graphics/2025-investment-outlooks/?embedded-checkout=true"
    
    try:
        # 1. Fetch and display content
        title, content = converter.fetch_content(url)
        print(f"\n=== Article Content ===")
        print(f"Title: {title}")
        print(f"\nFirst 1000 characters of content:")
        print(f"{content[:1000]}...")
        print("\n=== End of Preview ===\n")

        # 2. Create EPUB
        book = epub.EpubBook()
        book.set_identifier('bloomberg-article')
        book.set_title(title)
        book.set_language('en')

        # Add chapter
        c1 = epub.EpubHtml(title=title, file_name='article.xhtml')
        c1.content = f'<h1>{title}</h1><p>{content}</p>'
        book.add_item(c1)

        # Add to table of contents
        book.toc = [(epub.Section('Article'), [c1])]
        book.spine = ['nav', c1]

        # Save EPUB
        epub_path = os.path.join(converter.output_dir, 'article.epub')
        epub.write_epub(epub_path, book)
        print(f"Created EPUB file at: {epub_path}")

        # 3. Create MP3
        audio_path = converter.create_audio(title, content)
        print(f"Created MP3 file at: {audio_path}")

        # 4. Update podcast feed
        converter.update_podcast_feed(title, audio_path)
        print(f"Updated podcast feed at: {os.path.join(converter.output_dir, 'podcast.xml')}")

        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_bloomberg_article() 