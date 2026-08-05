"""Helpers for recognising progress-bar control lines in subprocess output.

Background scripts used by the GUI report progress on stdout via lines
of the form ``PROG:<N>`` where ``<N>`` is a percentage. The GUI's log
textbox should never display those control lines — they belong to the
progress bar widget — and ordinary log lines that *mention* ``PROG:``
inside a sentence (for example ``"Logging PROG:50 ok"``) should still
be visible to the user. Anchoring the match to the start of the line
keeps the two kinds of output cleanly separated.

This module is GUI-free on purpose so it can be unit tested without
pulling in customtkinter or tkinter.
"""

from __future__ import annotations

import re
from typing import Optional


# Match a stdout line that is *entirely* a ``PROG:<digits>`` directive,
# allowing optional surrounding whitespace and CR/LF trailers (``\r\n``,
# ``\n``, etc.). Substrings inside ordinary log messages will not match.
_PROG_LINE_RE = re.compile(r"^\s*PROG:(\d+)\s*$")


def parse_progress_line(text: Optional[str]) -> Optional[int]:
    """Return the integer percentage if ``text`` is a progress directive.

    Returns ``None`` for any line that is not a standalone ``PROG:<N>``
    directive — including empty strings, ordinary log messages that
    happen to contain ``PROG:`` mid-sentence, and ``PROG:<non-digits>``.
    """
    if not text:
        return None
    match = _PROG_LINE_RE.match(text)
    if match is None:
        return None
    try:
        return int(match.group(1))
    except (TypeError, ValueError):
        return None


def is_blank_console_line(text: Optional[str]) -> bool:
    """Return ``True`` for output chunks that should not reach the log.

    Progress-producing tools such as ``tqdm`` often emit standalone
    carriage returns or empty newline chunks while redrawing a progress
    line. Those chunks create visual blank rows in the GUI console, so the
    log textbox should ignore them entirely.
    """
    return text is None or text.strip() == ""
