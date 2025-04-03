import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final


@dataclass
class Txt2MdResult:
    input_folder: str
    output_folder: str
    processed_files: list[str]
    error: str | None = None


class Txt2MdConverter:
    encodings: Final = ("utf-8", "shift-jis", "iso-2022-jp", "euc-jp")

    def _copy_text(self, input_path: Path, output_path: Path) -> None:
        """
        Copy text from input file to output file.
        """
        for encoding in self.encodings:
            try:
                # Read the content of the txt file
                content = input_path.read_text(encoding=encoding)
                # Write the content to the md file
                output_path.write_text(content, encoding=encoding)
                # 成功したらおわり
                return
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError(encoding=",".join(self.encodings))

    def convert_txt_to_md(
        self, input_folder: str | Path, output_folder: str | Path
    ) -> Txt2MdResult:
        # Ensure output folder exists
        input_folder = Path(input_folder)
        output_folder = Path(output_folder)
        os.makedirs(output_folder, exist_ok=True)
        processed_files = []

        # Iterate through all files in the input folder
        for input_path in input_folder.glob("*.txt"):
            output_path = output_folder / input_path.with_suffix(".md").name
            self._copy_text(input_path, output_path)
            processed_files.append(str(output_path))
        return Txt2MdResult(
            input_folder=str(input_folder),
            output_folder=str(output_folder),
            processed_files=processed_files,
        )
