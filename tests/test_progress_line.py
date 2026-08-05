"""
tests/test_progress_line.py
============================
Unit tests for :mod:`utils.progress_line`.

This module intentionally has **no Spotify or GUI dependencies**, making it
very fast and entirely self-contained.

Covered functions
-----------------
- ``parse_progress_line``  — recognises ``PROG:<N>`` control lines.
- ``is_blank_console_line`` — filters tqdm carriage-return noise.
"""

import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from utils.progress_line import is_blank_console_line, parse_progress_line


# ===========================================================================
# parse_progress_line
# ===========================================================================

class TestParseProgressLine:
    """Tests that ``parse_progress_line`` returns the right integer or None."""

    # --- Lines that SHOULD be recognised ---

    def test_plain_progress_line(self):
        assert parse_progress_line("PROG:50\n") == 50

    def test_crlf_line_ending(self):
        assert parse_progress_line("PROG:0\r\n") == 0

    def test_leading_whitespace(self):
        assert parse_progress_line("  PROG:99\n") == 99

    def test_one_hundred_percent(self):
        assert parse_progress_line("PROG:100\n") == 100

    def test_zero_percent(self):
        assert parse_progress_line("PROG:0\n") == 0

    def test_no_trailing_newline(self):
        """A bare ``PROG:50`` with no newline should still match."""
        assert parse_progress_line("PROG:50") == 50

    # --- Lines that SHOULD NOT be recognised (returns None) ---

    def test_prog_substring_mid_sentence(self):
        """``PROG:`` inside an ordinary log line must NOT match."""
        assert parse_progress_line("Logging PROG:50 ok\n") is None

    def test_extra_text_after_number(self):
        assert parse_progress_line("PROG:50 then more\n") is None

    def test_non_numeric_value(self):
        assert parse_progress_line("PROG:abc\n") is None

    def test_empty_string(self):
        assert parse_progress_line("") is None

    def test_none_input(self):
        assert parse_progress_line(None) is None

    def test_plain_log_line(self):
        assert parse_progress_line("Doing stuff\n") is None

    def test_only_whitespace(self):
        assert parse_progress_line("   \n") is None

    @pytest.mark.parametrize("pct", [0, 1, 25, 50, 75, 99, 100])
    def test_various_valid_percentages(self, pct):
        assert parse_progress_line(f"PROG:{pct}\n") == pct


# ===========================================================================
# is_blank_console_line
# ===========================================================================

class TestIsBlankConsoleLine:
    """Tests that blank / whitespace-only output chunks are suppressed."""

    # --- Should be considered blank (True) ---

    def test_empty_string_is_blank(self):
        assert is_blank_console_line("") is True

    def test_newline_is_blank(self):
        assert is_blank_console_line("\n") is True

    def test_carriage_return_is_blank(self):
        assert is_blank_console_line("\r") is True

    def test_crlf_is_blank(self):
        assert is_blank_console_line("\r\n") is True

    def test_whitespace_crlf_is_blank(self):
        assert is_blank_console_line("   \r\n") is True

    def test_none_is_blank(self):
        assert is_blank_console_line(None) is True

    def test_spaces_only_is_blank(self):
        assert is_blank_console_line("     ") is True

    # --- Should NOT be considered blank (False) ---

    def test_log_line_is_not_blank(self):
        assert is_blank_console_line("Processing tracks\n") is False

    def test_prog_line_is_not_blank(self):
        """Progress lines carry information — they should not be suppressed."""
        assert is_blank_console_line("  PROG:50\n") is False

    def test_single_char_is_not_blank(self):
        assert is_blank_console_line("x") is False
