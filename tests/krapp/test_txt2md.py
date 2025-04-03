import pytest

from krapp.txt2md import Txt2MdConverter, Txt2MdResult


@pytest.fixture
def sut():
    return Txt2MdConverter()


def test_convert_txt_to_md(tmp_path, sut):
    # Setup: Create temporary input and output folders
    input_folder = tmp_path / "input"
    output_folder = tmp_path / "output"
    input_folder.mkdir()
    output_folder.mkdir()

    # Create sample .txt files in the input folder
    txt_file_1 = input_folder / "file1.txt"
    txt_file_2 = input_folder / "file2.txt"
    txt_file_1.write_text("Content of file1", encoding="utf-8")
    txt_file_2.write_text("Content of file2", encoding="utf-8")

    # Call the function
    result = sut.convert_txt_to_md(input_folder, output_folder)

    # Assertions
    assert isinstance(result, Txt2MdResult)
    assert result.input_folder == str(input_folder)
    assert result.output_folder == str(output_folder)
    assert len(result.processed_files) == 2

    # Check if the .md files were created with correct content
    md_file_1 = output_folder / "file1.md"
    md_file_2 = output_folder / "file2.md"
    assert md_file_1.exists()
    assert md_file_2.exists()
    assert md_file_1.read_text(encoding="utf-8") == "Content of file1"
    assert md_file_2.read_text(encoding="utf-8") == "Content of file2"


def test_convert_txt_to_md_shift_jis(tmp_path, sut):
    # Setup: Create temporary input and output folders
    input_folder = tmp_path / "input"
    output_folder = tmp_path / "output"
    input_folder.mkdir()
    output_folder.mkdir()

    # Create sample .txt files in the input folder
    txt_file_1 = input_folder / "file1.txt"
    txt_file_2 = input_folder / "file2.txt"
    txt_file_1.write_text("ファイル1", encoding="shift-jis")
    txt_file_2.write_text("ファイル2", encoding="shift-jis")

    # Call the function
    result = sut.convert_txt_to_md(input_folder, output_folder)

    # Assertions
    assert isinstance(result, Txt2MdResult)
    assert result.input_folder == str(input_folder)
    assert result.output_folder == str(output_folder)
    assert len(result.processed_files) == 2

    # Check if the .md files were created with correct content
    md_file_1 = output_folder / "file1.md"
    md_file_2 = output_folder / "file2.md"
    assert md_file_1.exists()
    assert md_file_2.exists()
    assert md_file_1.read_text(encoding="shift-jis") == "ファイル1"
    assert md_file_2.read_text(encoding="shift-jis") == "ファイル2"


def test_convert_txt_to_md_empty_input_folder(tmp_path, sut):
    # Setup: Create temporary input and output folders
    input_folder = tmp_path / "input"
    output_folder = tmp_path / "output"
    input_folder.mkdir()
    output_folder.mkdir()

    # Call the function with an empty input folder
    result = sut.convert_txt_to_md(input_folder, output_folder)

    # Assertions
    assert isinstance(result, Txt2MdResult)
    assert result.input_folder == str(input_folder)
    assert result.output_folder == str(output_folder)
    assert len(result.processed_files) == 0

    # Ensure no files were created in the output folder
    assert not any(output_folder.iterdir())
