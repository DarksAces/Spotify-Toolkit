import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --- CONFIGURACIÓN Y AUTENTICACIÓN ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

try:
    from utils.auth import get_spotify_client
    from utils.helpers import select_playlist, get_all_tracks
    sp = get_spotify_client()
except ImportError:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=["playlist-modify-public", "playlist-modify-private", "user-library-read"]
    ))

def main():
    while True:
        print("\n=== REORDER TRACKS (Mover artista al final) ===")
        mode, pl_id = select_playlist(sp, "SELECCIONA UNA LISTA", include_liked=True)
        
        if not mode: break
        if mode == "liked_songs":
            print("⚠️ No se puede reordenar 'Favoritos' vía API.")
            print("Se recomienda crear una nueva playlist.")
            continue

        tracks = get_all_tracks(sp, mode, pl_id)
        if not tracks: continue

        artist_target = input("\n🎤 Artista que quieres mover al final: ").lower().strip()
        
        # Encontrar índices de canciones del artista
        matches = []
        for i, item in enumerate(tracks):
            if not item['track']: continue
            track_artists = [a['name'].lower().strip() for a in item['track']['artists']]
            if any(artist_target in a for a in track_artists):
                matches.append(i)

        if not matches:
            print(f"⚠️ No se encontraron canciones de '{artist_target}'.")
            continue

        print(f"✅ Se han encontrado {len(matches)} canciones.")
        print("📤 Moviendo canciones al final...")
        
        total_tracks = len(tracks)
        for idx in sorted(matches, reverse=True):
            sp.playlist_reorder_items(pl_id, range_start=idx, insert_before=total_tracks)
        
        print(f"✅ ¡Hecho! {len(matches)} canciones movidas al final.")

        otra = input("\n¿Quieres reordenar otra? (s/n): ").strip().lower()
        if otra != 's': break

if __name__ == "__main__":
    main()
