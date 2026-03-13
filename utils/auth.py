import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys

def get_spotify_client(scope=None):
    """
    Returns an authenticated Spotify client.
    Default scope covers most toolkit operations.
    """
    if scope is None:
        scope = 'user-library-read user-top-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'
    
    # Environment variables are expected to be set by main_gui or .env
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

    if not all([client_id, client_secret, redirect_uri]):
        print("❌ Error: Missing Spotify credentials in environment variables.")
        sys.exit(1)

    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        open_browser=True
    ))
