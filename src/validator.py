"""Validator module for compiling and testing C++ solutions."""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple


class ValidationResult:
    """Represents the result of validation."""

    def __init__(self, success: bool, message: str, failed_cases: List[int] = None):
        """Initialize validation result.

        Args:
            success: Whether validation passed
            message: Success or error message
            failed_cases: List of failed test case indices (0-based)
        """
        self.success = success
        self.message = message
        self.failed_cases = failed_cases or []

    def __str__(self) -> str:
        """String representation."""
        return f"ValidationResult(success={self.success}, message={self.message})"


class SolutionValidator:
    """Validates C++ solutions by compiling and testing."""

    def __init__(self, code: str, samples: List[Dict[str, str]], timeout: int = 5):
        """Initialize validator.

        Args:
            code: C++ solution code
            samples: List of sample test cases with 'input' and 'output' keys
            timeout: Timeout for each test case in seconds
        """
        self.code = code
        self.samples = samples
        self.timeout = timeout
        self.work_dir = None

    def validate(self) -> ValidationResult:
        """Validate the solution by compiling and testing.

        Returns:
            ValidationResult object
        """
        # Create temporary working directory
        with tempfile.TemporaryDirectory() as tmpdir:
            self.work_dir = Path(tmpdir)

            # Step 1: Compile the code
            compile_result = self._compile()
            if not compile_result[0]:
                return ValidationResult(
                    success=False,
                    message=f"Compilation failed:\n{compile_result[1]}"
                )

            # Step 2: Run test cases
            test_result = self._run_tests()
            return test_result

    def _compile(self) -> Tuple[bool, str]:
        """Compile the C++ code.

        Returns:
            Tuple of (success, message)
        """
        source_file = self.work_dir / "solution.cpp"
        binary_file = self.work_dir / "solution"

        # Write source code
        source_file.write_text(self.code)

        # Compile with g++
        compile_cmd = [
            "g++",
            "-std=c++17",
            "-O2",
            "-o", str(binary_file),
            str(source_file)
        ]

        try:
            result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                return False, result.stderr

            return True, "Compilation successful"

        except subprocess.TimeoutExpired:
            return False, "Compilation timeout"
        except FileNotFoundError:
            return False, "g++ compiler not found. Please install g++."
        except Exception as e:
            return False, f"Compilation error: {str(e)}"

    def _run_tests(self) -> ValidationResult:
        """Run all sample test cases.

        Returns:
            ValidationResult object
        """
        binary_file = self.work_dir / "solution"
        failed_cases = []
        error_messages = []

        for i, sample in enumerate(self.samples):
            success, message = self._run_single_test(
                binary_file,
                sample['input'],
                sample['output'],
                i + 1
            )

            if not success:
                failed_cases.append(i)
                error_messages.append(f"Test case {i + 1}: {message}")

        if failed_cases:
            return ValidationResult(
                success=False,
                message="\n".join(error_messages),
                failed_cases=failed_cases
            )

        return ValidationResult(
            success=True,
            message=f"All {len(self.samples)} test cases passed!"
        )

    def _run_single_test(
        self,
        binary: Path,
        input_data: str,
        expected_output: str,
        case_number: int
    ) -> Tuple[bool, str]:
        """Run a single test case.

        Args:
            binary: Path to compiled binary
            input_data: Input string
            expected_output: Expected output string
            case_number: Test case number for error messages

        Returns:
            Tuple of (success, message)
        """
        try:
            result = subprocess.run(
                [str(binary)],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            if result.returncode != 0:
                return False, f"Runtime error (exit code {result.returncode}):\n{result.stderr}"

            actual_output = result.stdout.strip()
            expected_output = expected_output.strip()

            # Compare outputs (normalize whitespace)
            if self._normalize_output(actual_output) == self._normalize_output(expected_output):
                return True, "Passed"
            else:
                return False, (
                    f"Wrong answer\n"
                    f"Expected:\n{expected_output}\n"
                    f"Got:\n{actual_output}"
                )

        except subprocess.TimeoutExpired:
            return False, f"Time limit exceeded (>{self.timeout}s)"
        except Exception as e:
            return False, f"Execution error: {str(e)}"

    def _normalize_output(self, output: str) -> str:
        """Normalize output for comparison.

        Args:
            output: Output string

        Returns:
            Normalized output
        """
        # Split into lines, strip each line, filter empty lines
        lines = [line.strip() for line in output.split('\n')]
        lines = [line for line in lines if line]
        return '\n'.join(lines)


def validate_solution(code: str, samples: List[Dict[str, str]]) -> ValidationResult:
    """Convenience function to validate a solution.

    Args:
        code: C++ solution code
        samples: List of sample test cases

    Returns:
        ValidationResult object
    """
    validator = SolutionValidator(code, samples)
    return validator.validate()
