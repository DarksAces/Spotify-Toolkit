"""
conftest.py — Shared pytest fixtures for Spotify Toolkit tests.

All fixtures here are automatically available to every test module in the
`tests/` directory without any explicit import.
"""

import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Ensure the project root is importable (works for both `pytest` run from
# the project root and from inside the tests/ directory).
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ---------------------------------------------------------------------------
# Reusable sample data builders
# ---------------------------------------------------------------------------

def make_track(
    name="Test Song",
    artist="Test Artist",
    album="Test Album",
    uri="spotify:track:abc123",
    track_id="abc123",
    duration_ms=210000,
    popularity=75,
    release_date="2024-01-15",
    isrc="USABC1234567",
):
    """Return a fake Spotify *track object* (the inner dict inside a playlist item)."""
    return {
        "id": track_id,
        "name": name,
        "uri": uri,
        "duration_ms": duration_ms,
        "popularity": popularity,
        "artists": [{"name": artist, "id": "artist_id_001"}],
        "album": {
            "name": album,
            "release_date": release_date,
        },
        "external_ids": {"isrc": isrc},
    }


def make_playlist_item(track=None):
    """Return a fake Spotify *playlist item* wrapping a track dict."""
    if track is None:
        track = make_track()
    return {"track": track, "added_at": "2024-01-01T00:00:00Z"}


def make_playlist(
    name="My Playlist",
    playlist_id="pl_id_001",
    total_tracks=10,
):
    """Return a fake Spotify *playlist summary* as returned by current_user_playlists."""
    return {
        "id": playlist_id,
        "name": name,
        "tracks": {"total": total_tracks},
    }


def make_paged_response(items, total=None, has_next=False):
    """Wrap a list of items in a Spotify-style paged response dict."""
    return {
        "items": items,
        "total": total if total is not None else len(items),
        "next": "https://api.spotify.com/v1/next" if has_next else None,
        "limit": 50,
        "offset": 0,
    }


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_track():
    """A single fake Spotify track dict."""
    return make_track()


@pytest.fixture
def sample_playlist_item(sample_track):
    """A single fake Spotify playlist item (wraps a track)."""
    return make_playlist_item(sample_track)


@pytest.fixture
def sample_playlist():
    """A single fake Spotify playlist summary dict."""
    return make_playlist()


@pytest.fixture
def sample_tracks():
    """A list of three distinct fake playlist items."""
    return [
        make_playlist_item(make_track("Song A", "Artist A", track_id="id_a", uri="spotify:track:id_a")),
        make_playlist_item(make_track("Song B", "Artist B", track_id="id_b", uri="spotify:track:id_b")),
        make_playlist_item(make_track("Song C", "Artist C", track_id="id_c", uri="spotify:track:id_c")),
    ]


@pytest.fixture
def mock_sp():
    """
    A fully mocked ``spotipy.Spotify`` instance.

    Pre-configured with sensible defaults so individual tests only need to
    override the specific calls they care about.
    """
    sp = MagicMock()

    # current_user_playlists — returns one page of two playlists, no next page
    playlists = [make_playlist("Chill Vibes", "pl_001", 5), make_playlist("Workout Hits", "pl_002", 12)]
    sp.current_user_playlists.return_value = make_paged_response(playlists)

    # playlist_tracks — returns one page of three tracks, no next page
    tracks = [
        make_playlist_item(make_track("Song A", "Artist A", track_id="id_a", uri="spotify:track:id_a")),
        make_playlist_item(make_track("Song B", "Artist B", track_id="id_b", uri="spotify:track:id_b")),
        make_playlist_item(make_track("Song C", "Artist C", track_id="id_c", uri="spotify:track:id_c")),
    ]
    sp.playlist_tracks.return_value = make_paged_response(tracks)

    # current_user_saved_tracks — same shape
    sp.current_user_saved_tracks.return_value = make_paged_response(tracks)

    # sp.next() — no pagination; always returns None (single-page responses)
    sp.next.return_value = None

    # me() — user profile
    sp.me.return_value = {"id": "test_user_123", "display_name": "Test User"}

    return sp
