class ContentFormatter:
    """
    A class to format content for display.
    """

    def format_content(self, content: str) -> str:
        """
        Formats the content for display.

        Returns:
            str: The formatted content.
        """
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) > 2:
                front_matter = parts[1].strip()
                body = parts[2].strip()
            return f"```\n{front_matter}\n```\n\n{body}"
        return content
