import yaml


class YamlFrontmatterParser:
    """
    A simple YAML frontmatter parser.
    """

    def __init__(self):
        pass

    def has_frontmatter(self, content: str) -> bool:
        """
        Check if the content has YAML frontmatter.
        """
        return content.startswith("---") and "---" in content[3:]

    def split(self, content: str) -> tuple[str, str]:
        """
        Split the content into frontmatter and body.
        """
        if not self.has_frontmatter(content):
            return "", content

        end_index = content.find("---", 3)
        frontmatter = content[3:end_index].strip()
        body = content[end_index + 3 :].strip()
        return frontmatter, body

    def parse(self, content: str) -> dict:
        """
        Parse the YAML frontmatter from the content.
        """
        if not self.has_frontmatter(content):
            return {}
        yaml_content, _ = self.split(content)
        return yaml.safe_load(yaml_content)
