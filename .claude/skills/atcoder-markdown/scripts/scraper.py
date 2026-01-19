"""AtCoder problem scraper module."""

import re
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup


class AtCoderScraper:
    """Scraper for AtCoder problem pages."""

    def __init__(self, url: str):
        """Initialize scraper with problem URL.

        Args:
            url: AtCoder problem URL (e.g., https://atcoder.jp/contests/abc350/tasks/abc350_c)
        """
        self.url = url
        self.soup: Optional[BeautifulSoup] = None

    def fetch(self) -> Dict:
        """Fetch and parse the problem page.

        Returns:
            Dict containing structured problem data

        Raises:
            requests.RequestException: If fetching fails
            ValueError: If parsing fails
        """
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            self.soup = BeautifulSoup(response.text, 'html.parser')

            return self._parse_problem()
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch problem: {e}")

    def _parse_problem(self) -> Dict:
        """Parse problem data from HTML.

        Returns:
            Dict with keys: title, statement, constraints, input_format,
                           output_format, samples
        """
        if not self.soup:
            raise ValueError("Page not fetched yet")

        # Extract problem title
        title = self._extract_title()

        # Extract problem sections
        sections = self._extract_sections()

        # Extract sample test cases
        samples = self._extract_samples()

        return {
            'title': title,
            'statement': sections.get('statement', ''),
            'constraints': sections.get('constraints', ''),
            'input_format': sections.get('input', ''),
            'output_format': sections.get('output', ''),
            'samples': samples
        }

    def _extract_title(self) -> str:
        """Extract problem title."""
        title_tag = self.soup.find('span', class_='h2')
        if not title_tag:
            # Fallback to page title
            title_tag = self.soup.find('title')

        if title_tag:
            title = title_tag.get_text().strip()
            # Remove contest prefix if exists
            title = re.sub(r'^[A-Z]\s*-\s*', '', title)
            return title
        return "Unknown Problem"

    def _extract_sections(self) -> Dict[str, str]:
        """Extract problem sections (statement, constraints, input/output format).

        Returns:
            Dict with section names as keys
        """
        sections = {}

        # Find main problem content
        content = self.soup.find('div', id='task-statement')
        if not content:
            return sections

        # Extract problem statement (first part before any headers)
        parts = content.find_all(['p', 'h3', 'pre', 'ul', 'ol'])

        current_section = 'statement'
        current_text = []

        for part in parts:
            # Check if this is a section header
            if part.name == 'h3':
                # Save previous section
                if current_text:
                    sections[current_section] = '\n'.join(current_text).strip()
                    current_text = []

                # Determine new section
                header_text = part.get_text().strip().lower()
                if '制約' in header_text or 'constraint' in header_text:
                    current_section = 'constraints'
                elif '入力' in header_text or 'input' in header_text:
                    current_section = 'input'
                elif '出力' in header_text or 'output' in header_text:
                    current_section = 'output'
                else:
                    current_section = 'statement'
            else:
                # Add content to current section
                text = self._extract_text_content(part)
                if text:
                    current_text.append(text)

        # Save last section
        if current_text:
            sections[current_section] = '\n'.join(current_text).strip()

        return sections

    def _extract_text_content(self, element) -> str:
        """Extract text content preserving structure."""
        if element.name == 'pre':
            return f"```\n{element.get_text()}\n```"
        elif element.name in ['ul', 'ol']:
            items = element.find_all('li')
            return '\n'.join(f"- {item.get_text().strip()}" for item in items)
        else:
            return element.get_text().strip()

    def _extract_samples(self) -> List[Dict[str, str]]:
        """Extract sample input/output pairs.

        Returns:
            List of dicts with 'input' and 'output' keys
        """
        samples = []

        # Find all sample sections
        content = self.soup.find('div', id='task-statement')
        if not content:
            return samples

        # Look for Japanese or English sample headers
        sample_headers = content.find_all('h3')

        current_input = None
        current_output = None

        for header in sample_headers:
            header_text = header.get_text().strip()

            # Check if this is a sample input header
            if re.search(r'(入力例|Sample Input)\s*\d+', header_text, re.IGNORECASE):
                # Get the next <pre> tag
                pre = header.find_next('pre')
                if pre:
                    current_input = pre.get_text().strip()

            # Check if this is a sample output header
            elif re.search(r'(出力例|Sample Output)\s*\d+', header_text, re.IGNORECASE):
                # Get the next <pre> tag
                pre = header.find_next('pre')
                if pre:
                    current_output = pre.get_text().strip()

                    # If we have both input and output, save the pair
                    if current_input is not None:
                        samples.append({
                            'input': current_input,
                            'output': current_output
                        })
                        current_input = None
                        current_output = None

        return samples


def scrape_problem(url: str) -> Dict:
    """Convenience function to scrape an AtCoder problem.

    Args:
        url: AtCoder problem URL

    Returns:
        Dict containing structured problem data
    """
    scraper = AtCoderScraper(url)
    return scraper.fetch()
