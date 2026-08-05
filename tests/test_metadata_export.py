"""
tests/test_metadata_export.py
==============================
Unit tests for :mod:`metadata_export.metadata_export`.

The module-level ``sp = get_spotify_client()`` call is intercepted at import
time so these tests never hit the network.

Covered functions
-----------------
- ``flatten_track``    — flattens a raw Spotify playlist-item dict.
- ``export_to_csv``    — writes tracks to a CSV file.
- ``export_to_json``   — writes tracks to a JSON file.
"""

import sys
import os
import csv
import json
import tempfile
import pytest
from unittest.mock import patch, MagicMock

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.conftest import make_track, make_playlist_item

# ---------------------------------------------------------------------------
# Patch the Spotify client before importing the module under test so the
# module-level ``sp = get_spotify_client()`` never runs for real.
# ---------------------------------------------------------------------------
with patch("utils.auth.spotipy.Spotify"), patch("utils.auth.SpotifyOAuth"), \
     patch.dict("os.environ", {
         "SPOTIFY_CLIENT_ID": "fake_id",
         "SPOTIFY_CLIENT_SECRET": "fake_secret",
         "SPOTIFY_REDIRECT_URI": "http://localhost/cb",
     }):
    from metadata_export.metadata_export import flatten_track, export_to_csv, export_to_json


# ===========================================================================
# flatten_track
# ===========================================================================

class TestFlattenTrack:
    """Tests that a raw playlist item is correctly flattened for export."""

    def test_basic_fields_are_extracted(self):
        item = make_playlist_item(make_track(
            name="My Song",
            artist="Cool Artist",
            album="Great Album",
            uri="spotify:track:xyz",
            duration_ms=180_000,
            popularity=80,
            release_date="2023-06-01",
            isrc="USABC0987654",
        ))
        flat = flatten_track(item)

        assert flat["Name"] == "My Song"
        assert flat["Artists"] == "Cool Artist"
        assert flat["Album"] == "Great Album"
        assert flat["URI"] == "spotify:track:xyz"
        assert flat["Popularity"] == 80
        assert flat["ISRC"] == "USABC0987654"
        assert flat["Release Date"] == "2023-06-01"

    def test_multiple_artists_joined_with_comma(self):
        track = make_track()
        track["artists"] = [
            {"name": "Artist One"},
            {"name": "Artist Two"},
            {"name": "Artist Three"},
        ]
        flat = flatten_track({"track": track})
        assert flat["Artists"] == "Artist One, Artist Two, Artist Three"

    def test_returns_none_for_missing_track_key(self):
        assert flatten_track({}) is None

    def test_returns_none_for_null_track(self):
        assert flatten_track({"track": None}) is None

    def test_returns_none_for_empty_track(self):
        # An empty dict is falsy in the guard `if not track`
        assert flatten_track({"track": {}}) is None

    def test_duration_formatted_correctly(self):
        item = make_playlist_item(make_track(duration_ms=90_061_000))
        flat = flatten_track(item)
        assert flat["Duration"] == "1d 1h 1m 1s"

    def test_missing_isrc_returns_empty_string(self):
        track = make_track()
        track["external_ids"] = {}
        flat = flatten_track({"track": track})
        assert flat["ISRC"] == ""

    def test_empty_artists_list(self):
        track = make_track()
        track["artists"] = []
        flat = flatten_track({"track": track})
        assert flat["Artists"] == ""


# ===========================================================================
# export_to_csv
# ===========================================================================

class TestExportToCsv:
    """Tests for CSV writing — uses a real temp file, no mocking needed."""

    @pytest.fixture
    def sample_items(self):
        return [
            make_playlist_item(make_track("Song A", "Artist A", isrc="ISRC_A")),
            make_playlist_item(make_track("Song B", "Artist B", isrc="ISRC_B")),
        ]

    def test_creates_csv_with_expected_headers(self, sample_items, tmp_path):
        out = tmp_path / "out.csv"
        export_to_csv(sample_items, str(out))

        with open(out, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
        assert "Name" in headers
        assert "Artists" in headers
        assert "Album" in headers
        assert "ISRC" in headers

    def test_creates_csv_with_correct_row_count(self, sample_items, tmp_path):
        out = tmp_path / "out.csv"
        export_to_csv(sample_items, str(out))

        with open(out, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 2

    def test_csv_values_match_track_data(self, sample_items, tmp_path):
        out = tmp_path / "out.csv"
        export_to_csv(sample_items, str(out))

        with open(out, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert rows[0]["Name"] == "Song A"
        assert rows[1]["Name"] == "Song B"

    def test_migration_csv_uses_soundiiz_headers(self, sample_items, tmp_path):
        out = tmp_path / "migration.csv"
        export_to_csv(sample_items, str(out), is_migration=True)

        with open(out, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
        assert headers == ["title", "artist", "album", "isrc"]

    def test_migration_csv_maps_fields_correctly(self, sample_items, tmp_path):
        out = tmp_path / "migration.csv"
        export_to_csv(sample_items, str(out), is_migration=True)

        with open(out, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert rows[0]["title"] == "Song A"
        assert rows[0]["artist"] == "Artist A"
        assert rows[0]["isrc"] == "ISRC_A"

    def test_empty_track_list_does_not_create_file(self, tmp_path):
        out = tmp_path / "empty.csv"
        export_to_csv([], str(out))
        assert not out.exists()

    def test_null_track_items_are_skipped(self, tmp_path):
        items = [{"track": None}, make_playlist_item(make_track("Valid"))]
        out = tmp_path / "filtered.csv"
        export_to_csv(items, str(out))

        with open(out, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 1
        assert rows[0]["Name"] == "Valid"


# ===========================================================================
# export_to_json
# ===========================================================================

class TestExportToJson:
    """Tests for JSON writing."""

    @pytest.fixture
    def sample_items(self):
        return [
            make_playlist_item(make_track("Song A", "Artist A")),
            make_playlist_item(make_track("Song B", "Artist B")),
        ]

    def test_creates_valid_json_file(self, sample_items, tmp_path):
        out = tmp_path / "out.json"
        export_to_json(sample_items, str(out))
        with open(out, encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert len(data) == 2

    def test_json_contains_expected_fields(self, sample_items, tmp_path):
        out = tmp_path / "out.json"
        export_to_json(sample_items, str(out))
        with open(out, encoding="utf-8") as f:
            data = json.load(f)
        first = data[0]
        assert "Name" in first
        assert "Artists" in first
        assert "URI" in first

    def test_json_values_match_track_data(self, sample_items, tmp_path):
        out = tmp_path / "out.json"
        export_to_json(sample_items, str(out))
        with open(out, encoding="utf-8") as f:
            data = json.load(f)
        assert data[0]["Name"] == "Song A"
        assert data[1]["Artists"] == "Artist B"

    def test_empty_track_list_does_not_create_file(self, tmp_path):
        out = tmp_path / "empty.json"
        export_to_json([], str(out))
        assert not out.exists()

    def test_null_track_items_are_skipped(self, tmp_path):
        items = [{"track": None}, make_playlist_item(make_track("Valid"))]
        out = tmp_path / "filtered.json"
        export_to_json(items, str(out))
        with open(out, encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["Name"] == "Valid"
