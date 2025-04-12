import re
from dataclasses import dataclass
from datetime import datetime
from typing import Final, List


@dataclass(frozen=True)
class DatePatternFormat:
    pattern: str
    format: str


class DateExtractor:
    def __init__(self) -> None:
        # Define common date patterns
        self.date_patterns: Final[tuple[DatePatternFormat, ...]] = (
            DatePatternFormat(r"\b\d{4}-\d{2}-\d{2}\b", "%Y-%m-%d"),
            DatePatternFormat(r"\b\d{4}/\d{2}/\d{2}\b", "%Y/%m/%d"),
            DatePatternFormat(r"\b\d{2}-\d{2}-\d{4}\b", "%m-%d-%Y"),
            DatePatternFormat(r"\b\d{2}/\d{2}/\d{4}\b", "%m/%d/%Y"),
            DatePatternFormat(r"\d{4}年\d{1,2}月\d{1,2}日", "%Y年%m月%d日"),
            DatePatternFormat(r"\b\d{4}.\d{1,2}.\d{1,2}\b", "%Y.%m.%d"),
            DatePatternFormat(r"\b\d{8}\b", "%Y%m%d"),
            DatePatternFormat(r"\b(\d{8})_\d{4}\b", "%Y%m%d"),
        )

    def read_file(self, file_path: str) -> str:
        """Reads the content of a file and returns it as a string."""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def extract_dates_from_file(self, file_path: str) -> List[datetime]:
        """Reads a file and extracts dates from its content."""
        text = self.read_file(file_path)
        return self.extract_dates(text)

    def extract_dates(self, text: str) -> List[datetime]:
        """Extracts dates from the given text and returns them as a list of datetime objects."""
        dates = []
        for pattern in self.date_patterns:
            matches = re.findall(pattern.pattern, text)
            for match in matches:
                try:
                    dates.append(datetime.strptime(match, pattern.format))
                except ValueError:
                    # Skip invalid date formats
                    continue
        return dates
