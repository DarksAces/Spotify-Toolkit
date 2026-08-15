"""
utils/auth.py
=============
Spotify authentication for Spotify Toolkit.

Uses the **Authorization Code with PKCE** flow (RFC 7636) so that no
client secret needs to be embedded in the distributed executable.  Only
the ``SPOTIFY_CLIENT_ID`` environment variable is required at runtime;
``SPOTIFY_CLIENT_SECRET`` is never read.

Token cache
-----------
The OAuth token is stored in the current user's OS application-data
directory so that:
  - The cache survives reinstallation of the EXE (which may live in a
    read-only Program Files subdirectory).
  - Multiple OS users on the same machine each have their own cache.

  Windows : %APPDATA%\\SpotifyToolkit\\.cache
  macOS   : ~/Library/Application Support/SpotifyToolkit/.cache
  Linux   : ~/.local/share/SpotifyToolkit/.cache  (XDG fallback)

Error handling
--------------
Instead of calling ``sys.exit(1)`` directly, this module raises
``SpotifyAuthError`` (a ``RuntimeError`` subclass).  Callers — whether
the CLI, the GUI, or a unit test — can catch it and handle it
appropriately without the process being forcibly terminated.
"""

import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyPKCE
from spotipy.cache_handler import CacheFileHandler


# ---------------------------------------------------------------------------
# Public exception
# ---------------------------------------------------------------------------

class SpotifyAuthError(RuntimeError):
    """Raised when Spotify credentials are missing or authentication fails."""


# ---------------------------------------------------------------------------
# Default scope — broad enough for all current toolkit operations.
# Per-tool minimal scopes can be passed explicitly as needed.
# ---------------------------------------------------------------------------

DEFAULT_SCOPE = (
    "user-library-read "
    "user-top-read "
    "user-read-recently-played "
    "playlist-read-private "
    "playlist-read-collaborative "
    "playlist-modify-public "
    "playlist-modify-private"
)

# Redirect URI — must be registered in the Spotify Developer Dashboard.
DEFAULT_REDIRECT_URI = "http://127.0.0.1:8888/callback"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_cache_dir() -> str:
    """Return the OS-appropriate application-data directory for the toolkit."""
    if sys.platform == "win32":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    elif sys.platform == "darwin":
        base = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    else:
        # XDG_DATA_HOME or ~/.local/share
        base = os.environ.get("XDG_DATA_HOME") or os.path.join(os.path.expanduser("~"), ".local", "share")

    cache_dir = os.path.join(base, "SpotifyToolkit")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def _get_cache_path() -> str:
    """Return the full path to the OAuth token cache file."""
    return os.path.join(_get_cache_dir(), ".cache")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_cache_path() -> str:
    """Return the token-cache path (useful for the Logout handler in main.py)."""
    return _get_cache_path()


def get_spotify_client(scope: str | None = None) -> spotipy.Spotify:
    """
    Return an authenticated :class:`spotipy.Spotify` client.

    Uses the Authorization Code with PKCE flow.  On the first call (or
    after the cache has been cleared) a browser window will open so the
    user can authorise the app with their own Spotify account.  On
    subsequent calls the cached refresh token is used silently.

    Parameters
    ----------
    scope:
        Space-separated Spotify scopes.  Defaults to :data:`DEFAULT_SCOPE`.

    Raises
    ------
    SpotifyAuthError
        If ``SPOTIFY_CLIENT_ID`` is not set in the environment.
    """
    if scope is None:
        scope = DEFAULT_SCOPE

    client_id = os.getenv("SPOTIFY_CLIENT_ID", "").strip()
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", DEFAULT_REDIRECT_URI).strip()

    if not client_id:
        raise SpotifyAuthError(
            "SPOTIFY_CLIENT_ID is not set.  "
            "Add it to your .env file or set it as an environment variable."
        )

    cache_handler = CacheFileHandler(cache_path=_get_cache_path())

    auth_manager = SpotifyPKCE(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_handler=cache_handler,
        open_browser=True,
    )

    return spotipy.Spotify(
        auth_manager=auth_manager,
        requests_timeout=15,
        retries=3,
        status_retries=3,
        backoff_factor=0.5,
    )
