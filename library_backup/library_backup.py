import os
import sys
import spotipy
import json
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm

# --- CONFIGURACIÓN Y AUTENTICACIÓN ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

try:
    from utils.auth import get_spotify_client
    from utils.helpers import get_user_playlists, get_all_tracks, get_export_dir
    sp = get_spotify_client()
except ImportError:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope='user-library-read playlist-read-private'
    ))

def main():
    print("\n=== LIBRARY BACKUP (Copia de Seguridad Total) ===")
    print("Esta herramienta exportará todas tus playlists y canciones favoritas.")
    
    confirm = input("\n¿Deseas iniciar el respaldo completo? (s/n): ").strip().lower()
    if confirm != 's': return

    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    export_dir = get_export_dir()
    backup_dir = os.path.join(export_dir, f"Spotify_Backup_{date_str}")
    os.makedirs(backup_dir, exist_ok=True)

    print(f"\n📂 Los archivos se guardarán en la carpeta: {backup_dir}")

    # 1. Liked Songs
    print("\n📦 Respaldando 'Canciones Favoritas'...")
    liked_tracks = get_all_tracks(sp, "liked_songs")
    
    liked_data = []
    for item in liked_tracks:
        track = item.get('track')
        if track:
            liked_data.append({
                "name": track.get('name', 'Unknown'),
                "artists": ", ".join([a['name'] for a in track.get('artists', [])]),
                "album": track.get('album', {}).get('name', 'Unknown'),
                "uri": track.get('uri', '')
            })
            
    with open(os.path.join(backup_dir, "Liked_Songs.json"), 'w', encoding='utf-8') as f:
        json.dump(liked_data, f, indent=4, ensure_ascii=False)

    # 2. All Playlists
    playlists = get_user_playlists(sp)
    print(f"\n📦 Se han encontrado {len(playlists)} playlists para respaldar.")

    total_playlists = len(playlists)
    for idx, pl in enumerate(playlists):
        name = pl.get('name', f"Playlist_{idx}").replace(" ", "_").replace("/", "-").replace("\\", "-")
        print(f"\n[{idx+1}/{total_playlists}] Procesando: {name}")
        
        tracks = get_all_tracks(sp, "playlist", pl.get('id'))
        
        pl_data = []
        for item in tracks:
            track = item.get('track')
            if track:
                pl_data.append({
                    "name": track.get('name', 'Unknown'),
                    "artists": ", ".join([a['name'] for a in track.get('artists', [])]),
                    "album": track.get('album', {}).get('name', 'Unknown'),
                    "uri": track.get('uri', '')
                })
        
        filename = f"{name}.json"
        try:
            with open(os.path.join(backup_dir, filename), 'w', encoding='utf-8') as f:
                json.dump(pl_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error al guardar {filename}: {e}")
            
        # Progreso para la GUI
        percent = int(((idx + 1) / total_playlists) * 100)
        print(f"PROG:{min(percent, 100)}")
        sys.stdout.flush()

    print(f"\n✅ ¡Respaldo completado! Revisa la carpeta '{backup_dir}'.")

if __name__ == "__main__":
    main()
