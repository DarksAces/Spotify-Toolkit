import os
import sys

# Add project root to sys.path so `utils.progress_line` is importable.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from utils.progress_line import is_blank_console_line, parse_progress_line


def test_plain_progress_line_is_recognised():
    assert parse_progress_line("PROG:50\n") == 50


def test_progress_line_with_crlf_is_recognised():
    assert parse_progress_line("PROG:0\r\n") == 0


def test_progress_line_with_leading_whitespace_is_recognised():
    assert parse_progress_line("  PROG:99\n") == 99


def test_progress_line_at_one_hundred_is_recognised():
    assert parse_progress_line("PROG:100\n") == 100


def test_embedded_prog_substring_is_passed_through():
    # Real fix: ordinary log messages that happen to mention "PROG:"
    # mid-sentence must NOT be silenced. Previously the GUI used
    # `if "PROG:" in text` which incorrectly swallowed lines like this.
    assert parse_progress_line("Logging PROG:50 ok\n") is None


def test_progress_line_with_extra_text_is_passed_through():
    assert parse_progress_line("PROG:50 then more\n") is None


def test_non_numeric_progress_is_not_recognised():
    assert parse_progress_line("PROG:abc\n") is None


def test_empty_input_is_not_recognised():
    assert parse_progress_line("") is None
    assert parse_progress_line(None) is None


def test_plain_log_line_is_passed_through():
    assert parse_progress_line("Doing stuff\n") is None


def test_blank_console_line_is_suppressed():
    assert is_blank_console_line("")
    assert is_blank_console_line("\n")
    assert is_blank_console_line("\r")
    assert is_blank_console_line("\r\n")
    assert is_blank_console_line("   \r\n")
    assert is_blank_console_line(None)


def test_non_blank_console_line_is_not_suppressed():
    assert not is_blank_console_line("Processing tracks\n")
    assert not is_blank_console_line("  PROG:50\n")


if __name__ == "__main__":
    # Allow running directly: `python tests/test_progress_line.py`.
    test_plain_progress_line_is_recognised()
    test_progress_line_with_crlf_is_recognised()
    test_progress_line_with_leading_whitespace_is_recognised()
    test_progress_line_at_one_hundred_is_recognised()
    test_embedded_prog_substring_is_passed_through()
    test_progress_line_with_extra_text_is_passed_through()
    test_non_numeric_progress_is_not_recognised()
    test_empty_input_is_not_recognised()
    test_plain_log_line_is_passed_through()
    test_blank_console_line_is_suppressed()
    test_non_blank_console_line_is_not_suppressed()
    print("[OK] all parse_progress_line tests passed")
