"""LLM solver module using Claude API."""

import os
import re
from typing import Dict, Optional
import anthropic


class Solution:
    """Represents a solution with code and analysis."""

    def __init__(self, code: str, explanation: str, complexity: str = ""):
        """Initialize solution.

        Args:
            code: C++ solution code
            explanation: Explanation of the solution approach
            complexity: Complexity analysis
        """
        self.code = code
        self.explanation = explanation
        self.complexity = complexity

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary.

        Returns:
            Dict with code, explanation, and complexity
        """
        return {
            'code': self.code,
            'explanation': self.explanation,
            'complexity': self.complexity
        }


class ClaudeSolver:
    """Solver using Claude API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-5-20250929"):
        """Initialize Claude solver.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Claude model to use
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def solve(self, system_prompt: str, user_prompt: str) -> Solution:
        """Solve problem using Claude API.

        Args:
            system_prompt: System prompt for Claude
            user_prompt: User prompt with problem

        Returns:
            Solution object with code and analysis

        Raises:
            Exception: If API call fails or response parsing fails
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            response_text = message.content[0].text
            return self._parse_response(response_text)

        except anthropic.APIError as e:
            raise Exception(f"Claude API error: {e}")

    def _parse_response(self, response: str) -> Solution:
        """Parse Claude's response to extract code and explanation.

        Args:
            response: Raw response from Claude

        Returns:
            Solution object

        Raises:
            ValueError: If response format is invalid
        """
        # Extract C++ code from code blocks
        code_pattern = r'```(?:cpp|c\+\+)?\s*\n(.*?)```'
        code_matches = re.findall(code_pattern, response, re.DOTALL)

        if not code_matches:
            raise ValueError("No C++ code found in response")

        # Take the last code block (most likely to be the complete solution)
        code = code_matches[-1].strip()

        # Extract explanation (text before the code block)
        explanation_parts = []
        complexity = ""

        # Split response into sections
        sections = response.split('###')

        for section in sections:
            section = section.strip()
            if not section:
                continue

            # Check for explanation section
            if '解法' in section or '説明' in section or 'アルゴリズム' in section:
                # Remove code blocks from explanation
                explanation_text = re.sub(code_pattern, '', section, flags=re.DOTALL)
                explanation_parts.append(explanation_text.strip())

            # Extract complexity information
            if '計算量' in section or 'complexity' in section.lower():
                complexity = section.strip()

        explanation = '\n\n'.join(explanation_parts) if explanation_parts else "解法説明なし"

        return Solution(code=code, explanation=explanation, complexity=complexity)


def solve_problem(system_prompt: str, user_prompt: str, api_key: Optional[str] = None) -> Solution:
    """Convenience function to solve a problem.

    Args:
        system_prompt: System prompt for Claude
        user_prompt: User prompt with problem
        api_key: Optional API key (defaults to env var)

    Returns:
        Solution object
    """
    solver = ClaudeSolver(api_key=api_key)
    return solver.solve(system_prompt, user_prompt)
