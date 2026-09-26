import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path="reader.db"):
        self.db_path = db_path

        self.connection = sqlite3.connect(
            self.db_path
        )

        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                path TEXT UNIQUE NOT NULL,
                cover TEXT,
                date_added TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reading_progress (
                book_id INTEGER PRIMARY KEY,
                chapter INTEGER NOT NULL DEFAULT 0,
                position INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (book_id)
                    REFERENCES books(id)
                    ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                chapter INTEGER NOT NULL,
                position INTEGER NOT NULL,
                label TEXT,
                FOREIGN KEY (book_id)
                    REFERENCES books(id)
                    ON DELETE CASCADE
            )
        """)

        self.connection.commit()

    def add_book(
        self,
        title,
        author,
        path,
        cover=None,
    ):
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO books
            (title, author, path, cover, date_added)
            VALUES (?, ?, ?, ?, ?)
        """, (
            title,
            author,
            path,
            cover,
            datetime.now().isoformat(),
        ))

        self.connection.commit()

        cursor.execute("""
            SELECT id
            FROM books
            WHERE path = ?
        """, (path,))

        result = cursor.fetchone()

        return result[0] if result else None

    def get_book_by_path(self, path):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT id, title, author, path, cover
            FROM books
            WHERE path = ?
        """, (path,))

        result = cursor.fetchone()

        if result is None:
            return None

        return {
            "id": result[0],
            "title": result[1],
            "author": result[2],
            "path": result[3],
            "cover": result[4],
        }

    def save_progress(
        self,
        book_id,
        chapter,
        position,
    ):
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO reading_progress
            (book_id, chapter, position)
            VALUES (?, ?, ?)
            ON CONFLICT(book_id)
            DO UPDATE SET
                chapter = excluded.chapter,
                position = excluded.position
        """, (
            book_id,
            chapter,
            position,
        ))

        self.connection.commit()

    def get_progress(self, book_id):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT chapter, position
            FROM reading_progress
            WHERE book_id = ?
        """, (book_id,))

        result = cursor.fetchone()

        if result is None:
            return None

        return {
            "chapter": result[0],
            "position": result[1],
        }

    def close(self):
        self.connection.close()