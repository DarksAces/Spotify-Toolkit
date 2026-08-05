"""
tests/test_auth.py
==================
Unit tests for :mod:`utils.auth`.

No real Spotify client is ever created — ``spotipy.Spotify`` and
``spotipy.oauth2.SpotifyOAuth`` are patched at their *source* locations so
that ``importlib.reload(utils.auth)`` picks up the mocks instead of the
real classes.

Covered behaviour
-----------------
- ``get_spotify_client`` returns a Spotify instance when all credentials present.
- ``SpotifyOAuth`` is called with the correct env-var values.
- A custom ``scope`` argument is forwarded to ``SpotifyOAuth``.
- ``sys.exit(1)`` is raised when any credential env var is empty / missing.
"""

import sys
import os
import importlib
import pytest
from unittest.mock import patch, MagicMock

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_ENV = {
    "SPOTIFY_CLIENT_ID":     "fake_client_id_32chars_xxxxxxxxxxxx",
    "SPOTIFY_CLIENT_SECRET": "fake_client_secret_32chars_xxxxxx",
    "SPOTIFY_REDIRECT_URI":  "http://127.0.0.1:8888/callback",
}

# Patch the classes at their *source* so that reloading utils.auth still
# sees the mock (the 'from X import Y' re-executes on reload).
_P_OAUTH = "spotipy.oauth2.SpotifyOAuth"
_P_SP    = "spotipy.Spotify"


# ---------------------------------------------------------------------------
# Helper to reload utils.auth and return get_spotify_client while patches live
# ---------------------------------------------------------------------------

def _reload_and_get():
    """Reload utils.auth and return get_spotify_client (must be called inside patches)."""
    import utils.auth as _auth
    importlib.reload(_auth)
    return _auth.get_spotify_client


# ===========================================================================
# Tests
# ===========================================================================

class TestGetSpotifyClient:

    def test_returns_spotify_instance_with_valid_env(self):
        """Happy path — all env vars set → the Spotify instance is returned."""
        mock_instance = MagicMock()
        with patch(_P_SP, return_value=mock_instance), \
             patch(_P_OAUTH), \
             patch.dict("os.environ", VALID_ENV, clear=False):
            fn = _reload_and_get()
            result = fn()
        assert result is mock_instance

    def test_spotify_oauth_receives_correct_credentials(self):
        """SpotifyOAuth must be called with the env-var values."""
        with patch(_P_SP), \
             patch(_P_OAUTH) as mock_oauth, \
             patch.dict("os.environ", VALID_ENV, clear=False):
            fn = _reload_and_get()
            fn()

        mock_oauth.assert_called_once()
        _, call_kwargs = mock_oauth.call_args
        assert call_kwargs.get("client_id")     == VALID_ENV["SPOTIFY_CLIENT_ID"]
        assert call_kwargs.get("client_secret") == VALID_ENV["SPOTIFY_CLIENT_SECRET"]
        assert call_kwargs.get("redirect_uri")  == VALID_ENV["SPOTIFY_REDIRECT_URI"]

    def test_custom_scope_is_forwarded(self):
        """A caller-supplied scope must override the default."""
        with patch(_P_SP), \
             patch(_P_OAUTH) as mock_oauth, \
             patch.dict("os.environ", VALID_ENV, clear=False):
            fn = _reload_and_get()
            fn(scope="playlist-read-private")

        mock_oauth.assert_called_once()
        _, call_kwargs = mock_oauth.call_args
        assert call_kwargs.get("scope") == "playlist-read-private"

    def test_exits_when_client_id_missing(self):
        """sys.exit(1) when SPOTIFY_CLIENT_ID is empty."""
        env = dict(VALID_ENV, SPOTIFY_CLIENT_ID="")
        with patch.dict("os.environ", env, clear=False):
            fn = _reload_and_get()
            with pytest.raises(SystemExit) as exc_info:
                fn()
        assert exc_info.value.code == 1

    def test_exits_when_client_secret_missing(self):
        """sys.exit(1) when SPOTIFY_CLIENT_SECRET is empty."""
        env = dict(VALID_ENV, SPOTIFY_CLIENT_SECRET="")
        with patch.dict("os.environ", env, clear=False):
            fn = _reload_and_get()
            with pytest.raises(SystemExit) as exc_info:
                fn()
        assert exc_info.value.code == 1

    def test_exits_when_redirect_uri_missing(self):
        """sys.exit(1) when SPOTIFY_REDIRECT_URI is empty."""
        env = dict(VALID_ENV, SPOTIFY_REDIRECT_URI="")
        with patch.dict("os.environ", env, clear=False):
            fn = _reload_and_get()
            with pytest.raises(SystemExit) as exc_info:
                fn()
        assert exc_info.value.code == 1
