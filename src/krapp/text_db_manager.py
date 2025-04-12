from datetime import datetime
from pathlib import Path
from typing import Final

import pandas as pd
from sqlalchemy import Column, Date, Integer, String, create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from krapp.date_extractor import DateExtractor
from krapp.yaml_frontmatter_parser import YamlFrontmatterParser

Base = declarative_base()


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    char_count = Column(Integer)
    happiness_score = Column(Integer, nullable=True)


class TextDBManager:
    def __init__(
        self,
        folder_path: str | Path,
        date_extractor: DateExtractor,
        yaml_parser: YamlFrontmatterParser,
        db_path: str | Path | None = None,
    ):
        self.folder_path: Final = Path(folder_path)
        self.date_extractor: Final = date_extractor
        self.yaml_parser: Final = yaml_parser

        if db_path is None:
            db_url = "sqlite:///:memory:"
        else:
            db_url = f"sqlite:///{db_path}"

        self.engine: Final = create_engine(db_url)
        self._create_tables()

        self.session: Final = sessionmaker(bind=self.engine)()

    def _create_tables(self, recreate: bool = True):
        if recreate and inspect(self.engine).has_table("entries"):
            Entry.__table__.drop(self.engine)

        Base.metadata.create_all(self.engine)

    def _save_entry(self, title: str, content: str):
        # 文字数をカウント
        char_count = len(content) if content else 0
        # 日付を抽出
        date = self._extract_date(title, content)
        frontmatter = self.yaml_parser.parse(content)
        entry = Entry(
            date=date,
            title=title,
            content=content,
            char_count=char_count,
            happiness_score=frontmatter.get("happiness score", None),
        )
        self.session.add(entry)
        self.session.commit()
        print(f"Saved entry: {title}: {date}")

    def _extract_date(self, title: str, content: str) -> datetime | None:
        date_list = self.date_extractor.extract_dates(f"{title}\n{content}")
        # 日付が見つからない場合は、Noneを返す
        if len(date_list) == 0:
            return None
        # 最初に見つかった日付を返す
        return date_list[0]

    def process_folder(self):
        for file_path in self.folder_path.rglob("*.md"):
            if not file_path.is_file():
                continue
            try:
                title = file_path.stem
                content = file_path.read_text(encoding="utf-8")
                self._save_entry(
                    title=title,
                    content=content,
                )
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    def get_entries_by_year_month(self, year, month):
        query = (
            self.session.query(Entry)
            .filter(Entry.date.isnot(None), Entry.date.like(f"{year}-{month:02}-%"))
            .order_by(Entry.date.desc())
        )
        rows = [
            {
                "ID": entry.id,
                "Date": entry.date,
                "Title": entry.title,
                "Content": entry.content,
            }
            for entry in query.all()
        ]
        return pd.DataFrame(rows)

    def get_all_years(self):
        query = (
            self.session.query(Entry)
            .filter(Entry.date.isnot(None))
            .with_entities(Entry.date)
        )
        years = {entry.date.year for entry in query if entry.date}
        return sorted(years, reverse=True)

    def get_months_in_year(self, year):
        query = (
            self.session.query(Entry)
            .filter(Entry.date.isnot(None), Entry.date.like(f"{year}-%"))
            .with_entities(Entry.date)
        )
        months = {entry.date.month for entry in query if entry.date}
        return sorted(months)

    def close(self):
        self.session.close()
