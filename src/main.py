"""CLI entry point for AtCoder Problem Solver."""

import sys
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from src.scraper import scrape_problem
from src.parser import parse_to_markdown
from src.prompt import PromptBuilder
from src.solver import ClaudeSolver, Solution
from src.validator import SolutionValidator, ValidationResult

app = typer.Typer(
    name="atcoder-solver",
    help="AtCoder Problem Solver - Solve AtCoder problems using Claude AI",
    add_completion=False
)


def print_status(message: str, emoji: str = "🔄"):
    """Print status message."""
    typer.echo(f"{emoji} {message}")


def print_success(message: str):
    """Print success message."""
    typer.secho(f"✅ {message}", fg=typer.colors.GREEN, bold=True)


def print_error(message: str):
    """Print error message."""
    typer.secho(f"❌ {message}", fg=typer.colors.RED, bold=True)


def print_warning(message: str):
    """Print warning message."""
    typer.secho(f"⚠️  {message}", fg=typer.colors.YELLOW)


@app.command()
def solve(
    url: Annotated[str, typer.Argument(help="AtCoder problem URL")],
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Output directory")
    ] = Path("./output"),
    retry: Annotated[
        int,
        typer.Option("--retry", "-r", help="Maximum retry attempts for validation failures")
    ] = 3,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output")
    ] = False,
):
    """Solve an AtCoder problem using Claude AI.

    Example:
        atcoder-solver solve https://atcoder.jp/contests/abc350/tasks/abc350_c
    """
    try:
        # Create output directory
        output.mkdir(parents=True, exist_ok=True)

        # Step 1: Scrape problem
        print_status("Fetching problem from AtCoder...")
        problem_data = scrape_problem(url)
        print_success(f"Problem fetched: {problem_data['title']}")

        if verbose:
            typer.echo(f"  - Samples: {len(problem_data['samples'])} test cases")

        # Step 2: Parse to Markdown
        print_status("Converting to Markdown...")
        problem_markdown = parse_to_markdown(problem_data)

        # Save problem markdown
        problem_file = output / "problem.md"
        problem_file.write_text(problem_markdown, encoding='utf-8')
        print_success(f"Problem saved: {problem_file}")

        # Step 3: Build prompts
        print_status("Building prompts for Claude...")
        prompt_builder = PromptBuilder(problem_markdown)
        system_prompt = prompt_builder.build_system_prompt()
        user_prompt = prompt_builder.build_user_prompt()

        # Step 4: Solve with Claude
        solver = ClaudeSolver()
        solution: Optional[Solution] = None
        attempt = 0

        while attempt <= retry:
            if attempt == 0:
                print_status("Generating solution with Claude AI...")
                solution = solver.solve(system_prompt, user_prompt)
            else:
                print_warning(f"Retry attempt {attempt}/{retry}...")
                retry_prompt = prompt_builder.build_retry_prompt(
                    validation_result.message,
                    solution.code
                )
                solution = solver.solve(system_prompt, retry_prompt)

            print_success("Solution generated")

            if verbose:
                typer.echo(f"  - Code length: {len(solution.code)} characters")

            # Step 5: Validate solution
            print_status("Validating solution...")
            validator = SolutionValidator(solution.code, problem_data['samples'])
            validation_result: ValidationResult = validator.validate()

            if validation_result.success:
                print_success(validation_result.message)
                break
            else:
                print_error("Validation failed:")
                typer.echo(validation_result.message)

                if attempt >= retry:
                    print_error(f"Max retry attempts ({retry}) reached")
                    print_warning("Saving solution anyway...")
                    break

                attempt += 1

        # Step 6: Save output
        print_status("Saving solution files...")

        # Save solution code
        solution_file = output / "solution.cpp"
        solution_file.write_text(solution.code, encoding='utf-8')
        print_success(f"Solution saved: {solution_file}")

        # Save analysis
        analysis_content = f"# 解法説明\n\n{solution.explanation}\n"
        if solution.complexity:
            analysis_content += f"\n## 計算量\n\n{solution.complexity}\n"

        analysis_file = output / "analysis.md"
        analysis_file.write_text(analysis_content, encoding='utf-8')
        print_success(f"Analysis saved: {analysis_file}")

        # Final summary
        typer.echo("\n" + "=" * 50)
        if validation_result.success:
            print_success("Problem solved successfully! 🎉")
        else:
            print_warning("Solution generated but validation failed")
        typer.echo(f"Output directory: {output.absolute()}")
        typer.echo("=" * 50)

    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@app.command()
def version():
    """Show version information."""
    from src import __version__
    typer.echo(f"AtCoder Solver v{__version__}")


if __name__ == "__main__":
    app()
