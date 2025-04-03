import sqlite3
from datetime import datetime
from pathlib import Path

from krapp.date_extractor import DateExtractor


class TextDBManager:
    def __init__(
        self,
        folder_path: str,
        date_extractor: DateExtractor,
        db_path: str | None = None,
    ):
        self.folder_path = folder_path
        self.conn = self._get_db_connection(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()
        self.date_extractor = date_extractor

    def _get_db_connection(self, db_path: str | None):
        if db_path is None:
            return sqlite3.connect(":memory:")
        return sqlite3.connect(db_path)

    def _create_table(self, recreate: bool = True):
        if recreate:
            # 既存のテーブルを削除する
            self.cursor.execute("DROP TABLE IF EXISTS entries")
            self.conn.commit()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                title TEXT,
                content TEXT
            )
        """)
        self.conn.commit()

    def _save_entry(self, date: datetime | None, title: str, content: str):
        self.cursor.execute(
            "INSERT INTO entries (date, title, content) VALUES (?, ?, ?)",
            (date, title, content),
        )
        self.conn.commit()
        print(f"Saved entry: {title}: {date}")

    def process_folder(self):
        folder = Path(self.folder_path)
        for file_path in folder.rglob("*.md"):
            if not file_path.is_file():
                continue
            try:
                title = file_path.stem
                content = file_path.read_text(encoding="utf-8")
                date_list = self.date_extractor.extract_dates(f"{title}\n{content}")
                if len(date_list) > 0:
                    date = date_list[0]
                else:
                    date = None
                self._save_entry(
                    date=date,
                    title=title,
                    content=content,
                )
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    def close(self):
        self.conn.close()
