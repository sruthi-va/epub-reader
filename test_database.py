from reader.database import Database


def main():
    database = Database()

    book_id = database.add_book(
        title="Jane Eyre",
        author="Charlotte Brontë",
        path=r"C:\Users\sruth\Downloads\Jane_Eyre.epub",
    )

    print("Book ID:", book_id)

    database.save_progress(
        book_id=book_id,
        chapter=5,
        position=1200,
    )

    progress = database.get_progress(book_id)

    print("Progress:", progress)

    database.close()


if __name__ == "__main__":
    main()