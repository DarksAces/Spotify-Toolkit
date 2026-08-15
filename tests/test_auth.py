"""
tests/test_auth.py
==================
Unit tests for :mod:`utils.auth` — PKCE edition.

No real Spotify client is ever created.  ``spotipy.Spotify`` and
``spotipy.oauth2.SpotifyPKCE`` are patched at their *source* locations so
that ``importlib.reload(utils.auth)`` picks up the mocks instead of the
real classes.

Covered behaviour
-----------------
- ``get_spotify_client`` returns a Spotify instance when CLIENT_ID is present.
- ``SpotifyPKCE`` is called with the correct env-var values (no client_secret).
- A custom ``scope`` argument is forwarded to ``SpotifyPKCE``.
- ``SpotifyAuthError`` is raised (not SystemExit) when CLIENT_ID is missing.
- ``SpotifyAuthError`` is NOT raised when only REDIRECT_URI is absent
  (the module falls back to the built-in default).
- ``get_cache_path`` returns a path inside the OS app-data directory.
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
    "SPOTIFY_CLIENT_ID":    "fake_client_id_32chars_xxxxxxxxxxxx",
    "SPOTIFY_REDIRECT_URI": "http://127.0.0.1:8888/callback",
}

# Patch classes at their *source* so that reloading utils.auth still sees the
# mock (the 'from X import Y' re-executes on reload).
_P_PKCE  = "spotipy.oauth2.SpotifyPKCE"
_P_SP    = "spotipy.Spotify"
_P_CACHE = "spotipy.cache_handler.CacheFileHandler"


# ---------------------------------------------------------------------------
# Helper to reload utils.auth while patches are live
# ---------------------------------------------------------------------------

def _reload_and_get():
    """Reload utils.auth and return (get_spotify_client, SpotifyAuthError)."""
    import utils.auth as _auth
    importlib.reload(_auth)
    return _auth.get_spotify_client, _auth.SpotifyAuthError


# ===========================================================================
# Tests
# ===========================================================================

class TestGetSpotifyClient:

    def test_returns_spotify_instance_with_valid_env(self):
        """Happy path — CLIENT_ID set → the Spotify instance is returned."""
        mock_instance = MagicMock()
        with patch(_P_SP, return_value=mock_instance), \
             patch(_P_PKCE), \
             patch(_P_CACHE), \
             patch.dict("os.environ", VALID_ENV, clear=False):
            fn, _ = _reload_and_get()
            result = fn()
        assert result is mock_instance

    def test_spotify_pkce_receives_correct_credentials(self):
        """SpotifyPKCE must be called with client_id and redirect_uri — no secret."""
        with patch(_P_SP), \
             patch(_P_PKCE) as mock_pkce, \
             patch(_P_CACHE), \
             patch.dict("os.environ", VALID_ENV, clear=False):
            fn, _ = _reload_and_get()
            fn()

        mock_pkce.assert_called_once()
        _, call_kwargs = mock_pkce.call_args
        assert call_kwargs.get("client_id")    == VALID_ENV["SPOTIFY_CLIENT_ID"]
        assert call_kwargs.get("redirect_uri") == VALID_ENV["SPOTIFY_REDIRECT_URI"]
        # No client_secret should be passed at all
        assert "client_secret" not in call_kwargs

    def test_custom_scope_is_forwarded(self):
        """A caller-supplied scope must override the default."""
        with patch(_P_SP), \
             patch(_P_PKCE) as mock_pkce, \
             patch(_P_CACHE), \
             patch.dict("os.environ", VALID_ENV, clear=False):
            fn, _ = _reload_and_get()
            fn(scope="playlist-read-private")

        mock_pkce.assert_called_once()
        _, call_kwargs = mock_pkce.call_args
        assert call_kwargs.get("scope") == "playlist-read-private"

    def test_raises_spotify_auth_error_when_client_id_missing(self):
        """SpotifyAuthError (not SystemExit) when SPOTIFY_CLIENT_ID is empty."""
        env = dict(VALID_ENV, SPOTIFY_CLIENT_ID="")
        with patch.dict("os.environ", env, clear=False):
            fn, SpotifyAuthError = _reload_and_get()
            with pytest.raises(SpotifyAuthError):
                fn()

    def test_raises_spotify_auth_error_when_client_id_not_set(self):
        """SpotifyAuthError when SPOTIFY_CLIENT_ID is not in the environment at all."""
        env = {k: v for k, v in VALID_ENV.items() if k != "SPOTIFY_CLIENT_ID"}
        # Ensure the variable is absent
        with patch.dict("os.environ", env, clear=False):
            os.environ.pop("SPOTIFY_CLIENT_ID", None)
            fn, SpotifyAuthError = _reload_and_get()
            with pytest.raises(SpotifyAuthError):
                fn()

    def test_uses_default_redirect_uri_when_env_var_absent(self):
        """When SPOTIFY_REDIRECT_URI is not set, the built-in default is used."""
        env = {k: v for k, v in VALID_ENV.items() if k != "SPOTIFY_REDIRECT_URI"}
        with patch(_P_SP), \
             patch(_P_PKCE) as mock_pkce, \
             patch(_P_CACHE), \
             patch.dict("os.environ", env, clear=False):
            os.environ.pop("SPOTIFY_REDIRECT_URI", None)
            fn, _ = _reload_and_get()
            fn()

        _, call_kwargs = mock_pkce.call_args
        # Default redirect URI from auth.py
        assert call_kwargs.get("redirect_uri") == "http://127.0.0.1:8888/callback"


class TestGetCachePath:

    def test_cache_path_is_inside_app_data_dir(self):
        """get_cache_path() must return a path inside an OS app-data directory."""
        import utils.auth as auth
        cache = auth.get_cache_path()
        # Platform-agnostic: just verify the path includes 'SpotifyToolkit'
        assert "SpotifyToolkit" in cache
        # And that it ends with the expected filename
        assert cache.endswith(".cache")

    def test_cache_dir_is_created(self, tmp_path, monkeypatch):
        """The cache directory must be created if it does not already exist."""
        monkeypatch.setenv("APPDATA", str(tmp_path))
        monkeypatch.setattr(sys, "platform", "win32")
        import utils.auth as auth
        importlib.reload(auth)
        cache = auth.get_cache_path()
        assert os.path.isdir(os.path.dirname(cache))
