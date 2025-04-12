import os
import shutil
from datetime import datetime
from pathlib import Path

from krapp.date_extractor import DateExtractor


class DiaryOrganizer:
    def __init__(self, date_extractor: DateExtractor) -> None:
        self.date_extractor = date_extractor

    def organize_diary(
        self, input_md_file: str | Path, output_folder: str | Path, remove: bool = False
    ) -> None:
        # Read the content of the input markdown file
        input_md_file = Path(input_md_file)
        output_folder = Path(output_folder)
        content = input_md_file.read_text(encoding="utf-8")

        # Extract the date from the content
        date_list = self.date_extractor.extract_dates(
            f"{input_md_file.stem}\n{content}"
        )
        if len(date_list) == 0:
            raise ValueError(
                f"{input_md_file}. No valid date found in the markdown file."
            )
        date = date_list[0]

        if date == datetime.today():
            print(
                f"{input_md_file}. The date in the markdown file is today. No need to organize."
            )
            return

        # Create year and month folders
        year_folder = output_folder / str(date.year)
        month_folder = year_folder / f"{date.month:02d}"
        os.makedirs(month_folder, exist_ok=True)

        # 同じ名前のファイルがあった場合は処理をスキップ
        if month_folder.joinpath(input_md_file.name).exists():
            print(
                f"File {input_md_file.name} already exists in {month_folder}. Skipping."
            )
            return
        # Copy the markdown file to the appropriate folder
        shutil.copy(input_md_file, month_folder)
        if remove:
            os.remove(input_md_file)
