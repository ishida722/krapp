from krapp.yaml_frontmatter_parser import YamlFrontmatterParser


def test_split_with_frontmatter():
    content = """---
title: Test Title
author: Test Author
---
This is the body of the document."""
    parser = YamlFrontmatterParser()
    frontmatter, body = parser.split(content)
    assert frontmatter == "title: Test Title\nauthor: Test Author"
    assert body == "This is the body of the document."


def test_split_without_frontmatter():
    content = "This is the body of the document without frontmatter."
    parser = YamlFrontmatterParser()
    frontmatter, body = parser.split(content)
    assert frontmatter == ""
    assert body == "This is the body of the document without frontmatter."


def test_split_with_empty_content():
    content = ""
    parser = YamlFrontmatterParser()
    frontmatter, body = parser.split(content)
    assert frontmatter == ""
    assert body == ""


def test_split_with_only_frontmatter():
    content = """---
title: Test Title
author: Test Author
---"""
    parser = YamlFrontmatterParser()
    frontmatter, body = parser.split(content)
    assert frontmatter == "title: Test Title\nauthor: Test Author"
    assert body == ""


def test_has_frontmatter_with_valid_frontmatter():
    content = """---
title: Test Title
author: Test Author
---
This is the body of the document."""
    parser = YamlFrontmatterParser()
    assert parser.has_frontmatter(content) is True


def test_has_frontmatter_without_frontmatter():
    content = "This is the body of the document without frontmatter."
    parser = YamlFrontmatterParser()
    assert parser.has_frontmatter(content) is False


def test_has_frontmatter_with_empty_content():
    content = ""
    parser = YamlFrontmatterParser()
    assert parser.has_frontmatter(content) is False


def test_parse_with_valid_frontmatter():
    content = """---
title: Test Title
author: Test Author
---
This is the body of the document."""
    parser = YamlFrontmatterParser()
    parsed_data = parser.parse(content)
    assert parsed_data == {"title": "Test Title", "author": "Test Author"}


def test_parse_without_frontmatter():
    content = "This is the body of the document without frontmatter."
    parser = YamlFrontmatterParser()
    parsed_data = parser.parse(content)
    assert parsed_data == {}


def test_parse_with_empty_content():
    content = ""
    parser = YamlFrontmatterParser()
    parsed_data = parser.parse(content)
    assert parsed_data == {}


def test_parse_with_only_frontmatter():
    content = """---
title: Test Title
author: Test Author
---"""
    parser = YamlFrontmatterParser()
    parsed_data = parser.parse(content)
    assert parsed_data == {"title": "Test Title", "author": "Test Author"}
