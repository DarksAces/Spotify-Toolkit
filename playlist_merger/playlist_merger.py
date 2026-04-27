import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm

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
        scope='playlist-modify-public playlist-modify-private user-library-read'
    ))

def main():
    print("\n=== PLAYLIST MERGER (Fusionar Listas) ===")
    selected_playlists = []
    
    while True:
        print(f"\nHas seleccionado {len(selected_playlists)} playlists.")
        mode, pl_id = select_playlist(sp, "Elige una playlist para añadir a la fusión", include_liked=True)
        
        if not mode:
            if not selected_playlists: return
            break
            
        selected_playlists.append((mode, pl_id))
        otra = input("\n¿Añadir otra? (s/n): ").strip().lower()
        if otra != 's': break

    if not selected_playlists: return

    new_name = input("\nNombre para la nueva playlist: ").strip()
    if not new_name: new_name = "Fusión de Playlists"

    print("\n🚀 Recopilando todas las canciones...")
    all_uris = []
    for mode, pl_id in selected_playlists:
        tracks = get_all_tracks(sp, mode, pl_id)
        all_uris.extend([t['track']['uri'] for t in tracks if t['track'] and t['track'].get('uri')])

    if not all_uris:
        print("❌ No se encontraron canciones para fusionar.")
        return

    # Eliminar duplicados si el usuario quiere
    limpiar = input(f"\nSe encontraron {len(all_uris)} canciones en total. ¿Eliminar duplicados? (s/n): ").strip().lower()
    if limpiar == 's':
        all_uris = list(dict.fromkeys(all_uris))
        print(f"✅ Quedan {len(all_uris)} canciones únicas.")

    print("\n📤 Creando nueva playlist en Spotify...")
    user_id = sp.me()['id']
    new_pl = sp.user_playlist_create(user_id, new_name, public=False)
    
    total_uris = len(all_uris)
    with tqdm(total=total_uris, desc="Subiendo canciones", unit="track") as pbar:
        for i in range(0, total_uris, 100):
            batch = all_uris[i:i+100]
            sp.playlist_add_items(new_pl['id'], batch)
            pbar.update(len(batch))
            # Progreso para la GUI
            percent = int(((i + len(batch)) / total_uris) * 100)
            print(f"PROG:{min(percent, 100)}")
            sys.stdout.flush()
            
    print(f"\n✅ ¡Hecho! Playlist '{new_name}' creada con éxito.")

if __name__ == "__main__":
    main()
