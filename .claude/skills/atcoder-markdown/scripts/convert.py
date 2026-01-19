#!/usr/bin/env python3
"""AtCoder problem to Markdown converter."""

import sys
import argparse
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from scraper import scrape_problem
from parser import parse_to_markdown


def main():
    """Convert AtCoder problem to Markdown."""
    parser = argparse.ArgumentParser(
        description='Convert AtCoder problem to Markdown format'
    )
    parser.add_argument('url', help='AtCoder problem URL')
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: stdout)',
        type=Path
    )
    parser.add_argument(
        '--save-samples',
        help='Save sample test cases as JSON',
        type=Path
    )

    args = parser.parse_args()

    try:
        # Fetch problem
        print(f"Fetching problem from {args.url}...", file=sys.stderr)
        problem_data = scrape_problem(args.url)
        print(f"✓ Problem fetched: {problem_data['title']}", file=sys.stderr)

        # Convert to Markdown
        markdown = parse_to_markdown(problem_data)

        # Output
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(markdown, encoding='utf-8')
            print(f"✓ Markdown saved to {args.output}", file=sys.stderr)
        else:
            print(markdown)

        # Save samples if requested
        if args.save_samples:
            import json
            samples_data = {
                'samples': problem_data['samples'],
                'problem_title': problem_data['title']
            }
            args.save_samples.write_text(
                json.dumps(samples_data, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
            print(f"✓ Samples saved to {args.save_samples}", file=sys.stderr)

        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
