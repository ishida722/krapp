from unittest.mock import MagicMock, patch

import pytest

from krapp.date_extractor import DateExtractor
from krapp.diary_organizer import DiaryOrganizer


@pytest.fixture
def mock_date_extractor():
    mock = MagicMock(spec=DateExtractor)
    return mock


@pytest.fixture
def diary_organizer(mock_date_extractor):
    return DiaryOrganizer(date_extractor=mock_date_extractor)


def test_organize_diary_creates_correct_folders_and_copies_file(
    diary_organizer, mock_date_extractor, tmp_path
):
    # Arrange
    input_md_file = tmp_path / "test.md"
    output_folder = tmp_path / "output"
    input_md_file.write_text("Sample content with a date", encoding="utf-8")

    mock_date = MagicMock()
    mock_date.year = 2023
    mock_date.month = 5
    mock_date_extractor.extract_dates.return_value = [mock_date]

    # Act
    diary_organizer.organize_diary(input_md_file, output_folder)

    # Assert
    expected_folder = output_folder / "2023" / "05"
    assert expected_folder.exists()
    assert (expected_folder / "test.md").exists()


def test_organize_diary_raises_error_when_no_date_found(
    diary_organizer, mock_date_extractor, tmp_path
):
    # Arrange
    input_md_file = tmp_path / "test.md"
    output_folder = tmp_path / "output"
    input_md_file.write_text("Content without a date", encoding="utf-8")

    mock_date_extractor.extract_dates.return_value = []

    # Act & Assert
    with pytest.raises(ValueError, match="No valid date found in the markdown file."):
        diary_organizer.organize_diary(input_md_file, output_folder)


@patch("shutil.copy")
def test_organize_diary_calls_shutil_copy(
    mock_copy, diary_organizer, mock_date_extractor, tmp_path
):
    # Arrange
    input_md_file = tmp_path / "test.md"
    output_folder = tmp_path / "output"
    input_md_file.write_text("Sample content with a date", encoding="utf-8")

    mock_date = MagicMock()
    mock_date.year = 2023
    mock_date.month = 5
    mock_date_extractor.extract_dates.return_value = [mock_date]

    # Act
    diary_organizer.organize_diary(input_md_file, output_folder)

    # Assert
    expected_folder = output_folder / "2023" / "05"
    mock_copy.assert_called_once_with(input_md_file, expected_folder)
