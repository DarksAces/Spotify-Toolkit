import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --- CONFIGURACIÓN Y AUTENTICACIÓN ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

try:
    from utils.auth import get_spotify_client
    from utils.helpers import select_playlist, format_duration
    sp = get_spotify_client()
except ImportError:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope='playlist-read-private playlist-read-collaborative'
    ))

def calculate_playlist_duration(playlist_id, name):
    print(f"⌛ Calculando duración de '{name}'...")
    total_duration_ms = 0
    track_count = 0
    offset = 0
    
    while True:
        results = sp.playlist_tracks(playlist_id, offset=offset, fields="items.track(duration_ms),next")
        items = results['items']
        for item in items:
            if item and item['track']:
                total_duration_ms += item['track']['duration_ms']
                track_count += 1
        
        if not results['next']: break
        offset += len(items)
        print(f"   ∟ Procesadas {track_count} canciones...")
    
    return total_duration_ms, track_count

def main():
    while True:
        print("\n=== CALCULADOR DE TIEMPO (Playlist Duration) ===")
        mode, pl_id = select_playlist(sp, "Elige una lista para calcular su duración", include_liked=True)
        
        if not mode: break
        
        print(f"⌛ Obteniendo información...")
        
        total_duration_ms = 0
        track_count = 0
        
        try:
            if mode == "liked_songs":
                results = sp.current_user_saved_tracks(limit=50)
            else:
                results = sp.playlist_tracks(pl_id, limit=50, fields="items.track(duration_ms),next")
            
            while results:
                items = results['items']
                for item in items:
                    if item and item['track']:
                        total_duration_ms += item['track']['duration_ms']
                        track_count += 1
                
                if results['next']:
                    results = sp.next(results)
                    print(f"   ∟ Procesadas {track_count} canciones...")
                else:
                    results = None
        except Exception as e:
            print(f"❌ Error al obtener canciones: {e}")
            continue

        print("\n" + "="*40)
        print(f"📊 RESUMEN:")
        print(f"🎵 Canciones: {track_count}")
        print(f"⏱️ Duración total: {format_duration(total_duration_ms)}")
        print("="*40)
        
        otra = input("\n¿Quieres calcular otra? (s/n): ").strip().lower()
        if otra != 's': break

if __name__ == "__main__":
    main()
