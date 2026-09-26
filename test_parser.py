from epub.parser import EPUBParser


EPUB_PATH = r"C:\Users\sruth\Downloads\Monstrilio _ A Novel -- Gerardo Sámano Córdova -- Lightning Source Inc_ (Tier 1), New York, 2023 -- Zando -- isbn13 9781638930365 -- d1f9be176ea6d5e22e95510a0a3884fa -- Anna’s Archive.epub"


def main():
    parser = EPUBParser(EPUB_PATH)
    book = parser.parse()

    print("=" * 40)
    print("BOOK")
    print("=" * 40)

    print("Title:", book.title)
    print("Author:", book.author)
    print("Language:", book.language)
    print("Identifier:", book.identifier)
    print("Cover:", book.cover)

    print("\n" + "-" * 40)
    print("CHAPTERS")
    print("-" * 40)

    for index, chapter in enumerate(book.chapters, start=1):
        print(f"{index}. {chapter.title}")
        print(f"   {chapter.href}")
        print(f"   Content length: {len(chapter.content)}")


if __name__ == "__main__":
    main()