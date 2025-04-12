from datetime import datetime

import pytest

from krapp.date_extractor import DateExtractor


@pytest.fixture
def extractor():
    return DateExtractor()


def test_extract_dates_with_yyyy_mm_dd(extractor):
    text = "The event is scheduled for 2023-10-15."
    expected = [datetime(2023, 10, 15)]
    result = extractor.extract_dates(text)
    assert result == expected


def test_extract_dates_sample1(extractor):
    text = """
---
created: 2024-12-17
tags:
---
    """
    expected = [datetime(2024, 12, 17)]
    result = extractor.extract_dates(text)
    assert result == expected


def test_extract_dates_sample2(extractor):
    text = """
タイトル

2024/10/21 22:09

    """
    expected = [datetime(2024, 10, 21)]
    result = extractor.extract_dates(text)
    assert result == expected


def test_extract_dates_sample3(extractor):
    text = """2024/10/21.md"""
    expected = [datetime(2024, 10, 21)]
    result = extractor.extract_dates(text)
    assert result == expected


def test_extract_dates_sample4(extractor):
    text = """2024/10/21タイトル.md"""
    expected = []
    result = extractor.extract_dates(text)
    assert result == expected


def test_extract_dates_sample5(extractor):
    text = """2024-10-21_タイトル.md"""
    expected = []
    result = extractor.extract_dates(text)
    assert result == expected


def test_extract_dates_sample6(extractor):
    text = """
# タイトル
[2015-02-09 16:54]
    """
    expected = [datetime(2015, 2, 9)]
    result = extractor.extract_dates(text)
    assert result == expected


def test_extract_dates_with_mm_dd_yyyy(extractor):
    text = "The event is scheduled for 10/15/2023."
    expected = [datetime(2023, 10, 15)]
    result = extractor.extract_dates(text)
    assert result == expected


def test_extract_dates_with_yyyymmdd(extractor):
    text = "20231015.md"
    expected = [datetime(2023, 10, 15)]
    result = extractor.extract_dates(text)
    assert result == expected


def test_extract_dates_with_yyyymmdd_time(extractor):
    text = "20231015_1749.md"
    expected = [datetime(2023, 10, 15)]
    result = extractor.extract_dates(text)
    assert result == expected


def test_extract_dates_with_mm_dd_yyyy_hyphen(extractor):
    text = "The event is scheduled for 10-15-2023."
    expected = [datetime(2023, 10, 15)]
    result = extractor.extract_dates(text)
    assert result == expected


def test_extract_dates_with_yyyy_mm_dd_slash(extractor):
    text = "The event is scheduled for 2023/10/15."
    expected = [datetime(2023, 10, 15)]
    result = extractor.extract_dates(text)
    assert result == expected


def test_extract_dates_with_japanese_format(extractor):
    text = "イベントは2023年10月15日に予定されています。"
    expected = [datetime(2023, 10, 15)]
    result = extractor.extract_dates(text)
    assert result == expected


def test_extract_dates_with_multiple_formats(extractor):
    text = "Dates: 2023-10-15, 10/15/2023, 10-15-2023, and 2023/10/15 are all valid."
    expected = [
        datetime(2023, 10, 15),
        datetime(2023, 10, 15),
        datetime(2023, 10, 15),
        datetime(2023, 10, 15),
    ]
    result = extractor.extract_dates(text)
    assert result == expected


def test_extract_dates_with_invalid_dates(extractor):
    text = "Invalid dates like 2023-15-10 or 99/99/9999 should be ignored."
    result = extractor.extract_dates(text)
    assert result == []


def test_extract_dates_with_no_dates(extractor):
    text = "There are no dates in this text."
    result = extractor.extract_dates(text)
    assert result == []
