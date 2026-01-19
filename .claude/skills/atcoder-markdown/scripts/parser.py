"""Parser module to convert problem data to Markdown format."""

from typing import Dict, List


class MarkdownParser:
    """Converts structured problem data to Markdown format."""

    def __init__(self, problem_data: Dict):
        """Initialize parser with problem data.

        Args:
            problem_data: Dict from scraper containing problem information
        """
        self.data = problem_data

    def to_markdown(self) -> str:
        """Convert problem data to Markdown format.

        Returns:
            Formatted Markdown string
        """
        sections = []

        # Title
        sections.append(f"# {self.data.get('title', 'Unknown Problem')}\n")

        # Problem Statement
        if self.data.get('statement'):
            sections.append("## 問題文\n")
            sections.append(f"{self.data['statement']}\n")

        # Constraints
        if self.data.get('constraints'):
            sections.append("## 制約\n")
            sections.append(f"{self.data['constraints']}\n")

        # Input Format
        if self.data.get('input_format'):
            sections.append("## 入力形式\n")
            sections.append(f"{self.data['input_format']}\n")

        # Output Format
        if self.data.get('output_format'):
            sections.append("## 出力形式\n")
            sections.append(f"{self.data['output_format']}\n")

        # Sample Cases
        samples = self.data.get('samples', [])
        if samples:
            sections.append("## サンプル\n")
            for i, sample in enumerate(samples, 1):
                sections.append(f"### 入力例{i}\n")
                sections.append("```")
                sections.append(sample.get('input', ''))
                sections.append("```\n")

                sections.append(f"### 出力例{i}\n")
                sections.append("```")
                sections.append(sample.get('output', ''))
                sections.append("```\n")

        return '\n'.join(sections)


def parse_to_markdown(problem_data: Dict) -> str:
    """Convenience function to convert problem data to Markdown.

    Args:
        problem_data: Dict from scraper containing problem information

    Returns:
        Formatted Markdown string
    """
    parser = MarkdownParser(problem_data)
    return parser.to_markdown()
