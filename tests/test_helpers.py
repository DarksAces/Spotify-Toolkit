"""
tests/test_helpers.py
=====================
Unit tests for :mod:`utils.helpers`.

Covered functions
-----------------
- ``format_duration``    — pure formatting logic, no Spotify calls needed.
- ``get_user_playlists`` — fetches paginated playlists via the Spotify client.
- ``get_all_tracks``     — fetches paginated tracks for a playlist or Liked Songs.
"""

import sys
import os

# ---------------------------------------------------------------------------
# Ensure UTF-8 output on Windows so emoji in print() don't crash the runner.
# ---------------------------------------------------------------------------
if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import pytest
from unittest.mock import MagicMock, patch, call

# conftest.py already adds the project root to sys.path, but guard here too.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.helpers import format_duration, get_user_playlists, get_all_tracks
from tests.conftest import make_track, make_playlist_item, make_playlist, make_paged_response


# ===========================================================================
# format_duration
# ===========================================================================

class TestFormatDuration:
    """Pure unit tests — no mocking required."""

    def test_none_returns_zero(self):
        assert format_duration(None) == "0s"

    def test_non_numeric_string_returns_zero(self):
        assert format_duration("not a number") == "0s"

    def test_zero_ms_returns_zero(self):
        assert format_duration(0) == "0s"

    def test_one_second(self):
        assert format_duration(1_000) == "1s"

    def test_one_minute_one_second(self):
        assert format_duration(61_000) == "1m 1s"

    def test_one_hour_one_minute_one_second(self):
        assert format_duration(3_661_000) == "1h 1m 1s"

    def test_one_day_one_hour_one_minute_one_second(self):
        assert format_duration(90_061_000) == "1d 1h 1m 1s"

    def test_exactly_one_minute(self):
        assert format_duration(60_000) == "1m"

    def test_float_value_is_accepted(self):
        # floats are valid — e.g. when duration_ms comes from JSON as float
        result = format_duration(3_661_000.0)
        assert result == "1h 1m 1s"

    def test_large_duration(self):
        # 2 days, 3 hours, 4 minutes, 5 seconds
        ms = (2 * 86_400 + 3 * 3_600 + 4 * 60 + 5) * 1_000
        assert format_duration(ms) == "2d 3h 4m 5s"


# ===========================================================================
# get_user_playlists
# ===========================================================================

class TestGetUserPlaylists:
    """Tests for the paginated playlist fetcher."""

    def test_returns_all_playlists_single_page(self, mock_sp):
        """Single-page response — all items returned directly."""
        result = get_user_playlists(mock_sp)
        assert len(result) == 2
        assert result[0]["name"] == "Chill Vibes"
        assert result[1]["name"] == "Workout Hits"

    def test_calls_current_user_playlists_once_for_single_page(self, mock_sp):
        get_user_playlists(mock_sp)
        mock_sp.current_user_playlists.assert_called_once()

    def test_paginates_across_multiple_pages(self, mock_sp):
        """When ``next`` is not None the helper keeps fetching."""
        page1_playlists = [make_playlist("Page 1 PL", "p1", 3)]
        page2_playlists = [make_playlist("Page 2 PL", "p2", 7)]

        page1 = make_paged_response(page1_playlists, has_next=True)
        page2 = make_paged_response(page2_playlists, has_next=False)

        mock_sp.current_user_playlists.return_value = page1
        mock_sp.next.side_effect = [page2, None]

        result = get_user_playlists(mock_sp)
        assert len(result) == 2
        assert result[0]["name"] == "Page 1 PL"
        assert result[1]["name"] == "Page 2 PL"

    def test_returns_empty_list_on_api_error(self, mock_sp):
        """API errors are swallowed; an empty list is returned."""
        mock_sp.current_user_playlists.side_effect = Exception("Network error")
        result = get_user_playlists(mock_sp)
        assert result == []

    def test_returns_empty_list_when_no_playlists(self, mock_sp):
        mock_sp.current_user_playlists.return_value = make_paged_response([])
        result = get_user_playlists(mock_sp)
        assert result == []


# ===========================================================================
# get_all_tracks
# ===========================================================================

class TestGetAllTracks:
    """Tests for the paginated track fetcher."""

    def test_fetches_playlist_tracks(self, mock_sp):
        """Normal playlist mode returns the expected tracks."""
        result = get_all_tracks(mock_sp, "playlist", "pl_001")
        # conftest mock has 3 valid tracks with IDs
        assert len(result) == 3
        mock_sp.playlist_tracks.assert_called_once_with("pl_001")

    def test_fetches_liked_songs(self, mock_sp):
        """Liked Songs mode uses current_user_saved_tracks."""
        result = get_all_tracks(mock_sp, "liked_songs")
        assert len(result) == 3
        mock_sp.current_user_saved_tracks.assert_called_once()

    def test_filters_out_items_without_track(self, mock_sp):
        """Items where 'track' is None or missing are discarded."""
        items = [
            {"track": None},                              # null track
            {},                                           # missing key entirely
            make_playlist_item(make_track("Valid", track_id="valid_id")),
        ]
        mock_sp.playlist_tracks.return_value = make_paged_response(items)
        result = get_all_tracks(mock_sp, "playlist", "pl_001")
        assert len(result) == 1
        assert result[0]["track"]["name"] == "Valid"

    def test_filters_out_tracks_without_id(self, mock_sp):
        """Tracks with no 'id' field are discarded (local files, podcasts, etc.)."""
        no_id_track = make_track("No ID Track")
        no_id_track["id"] = None
        items = [
            make_playlist_item(no_id_track),
            make_playlist_item(make_track("Has ID", track_id="real_id")),
        ]
        mock_sp.playlist_tracks.return_value = make_paged_response(items)
        result = get_all_tracks(mock_sp, "playlist", "pl_001")
        assert len(result) == 1
        assert result[0]["track"]["name"] == "Has ID"

    def test_returns_empty_list_on_api_error(self, mock_sp):
        """API errors are swallowed; an empty list is returned."""
        mock_sp.playlist_tracks.side_effect = Exception("Timeout")
        result = get_all_tracks(mock_sp, "playlist", "pl_001")
        assert result == []

    def test_paginates_across_multiple_pages(self, mock_sp):
        """When the API returns a 'next' URL the helper fetches subsequent pages."""
        page1_items = [make_playlist_item(make_track("Track 1", track_id="t1"))]
        page2_items = [make_playlist_item(make_track("Track 2", track_id="t2"))]

        page1 = make_paged_response(page1_items, total=2, has_next=True)
        page2 = make_paged_response(page2_items, total=2, has_next=False)

        mock_sp.playlist_tracks.return_value = page1
        mock_sp.next.side_effect = [page2, None]

        result = get_all_tracks(mock_sp, "playlist", "pl_001")
        assert len(result) == 2
        names = [r["track"]["name"] for r in result]
        assert "Track 1" in names
        assert "Track 2" in names


# ===========================================================================
# Playlist search / selection helper logic (pure Python, no Spotify calls)
# ===========================================================================

class TestPlaylistSearchLogic:
    """
    The name-based search inside select_playlist is pure Python logic.
    We test it directly against a list of dicts — no mock Spotify needed.
    """

    PLAYLISTS = [
        {"name": "Rock Mix", "tracks": {"total": 10}},
        {"name": None, "tracks": None},       # malformed entry
        {"tracks": {"total": 5}},             # missing name key
        {"name": "Jazz Party", "tracks": {"total": 8}},
    ]

    def _search(self, choice):
        return [
            pl
            for pl in self.PLAYLISTS
            if isinstance(pl, dict) and choice.lower() in (pl.get("name") or "").lower()
        ]

    def test_exact_match_found(self):
        matches = self._search("Rock Mix")
        assert len(matches) == 1
        assert matches[0]["name"] == "Rock Mix"

    def test_partial_case_insensitive_match(self):
        matches = self._search("rock")
        assert len(matches) == 1

    def test_no_match_returns_empty(self):
        matches = self._search("Metal")
        assert len(matches) == 0

    def test_malformed_entries_do_not_raise(self):
        """None names and missing name keys must not raise exceptions."""
        matches = self._search("jazz")
        assert len(matches) == 1
        assert matches[0]["name"] == "Jazz Party"
