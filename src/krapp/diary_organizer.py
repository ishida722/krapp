import os
import shutil
from pathlib import Path

from krapp.date_extractor import DateExtractor


class DiaryOrganizer:
    def __init__(self, date_extractor: DateExtractor) -> None:
        self.date_extractor = date_extractor

    def organize_diary(
        self, input_md_file: str | Path, output_folder: str | Path
    ) -> None:
        # Read the content of the input markdown file
        input_md_file = Path(input_md_file)
        output_folder = Path(output_folder)
        content = input_md_file.read_text(encoding="utf-8")

        # Extract the date from the content
        date_list = self.date_extractor.extract_dates(content)
        if len(date_list) == 0:
            raise ValueError("No valid date found in the markdown file.")
        date = date_list[0]

        # Create year and month folders
        year_folder = output_folder / str(date.year)
        month_folder = year_folder / f"{date.month:02d}"
        os.makedirs(month_folder, exist_ok=True)

        # Copy the markdown file to the appropriate folder
        shutil.copy(input_md_file, month_folder)
