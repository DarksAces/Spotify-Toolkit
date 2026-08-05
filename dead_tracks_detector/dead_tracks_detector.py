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
        scope='playlist-read-private playlist-modify-public playlist-modify-private user-library-read'
    ))

def main():
    print("\n=== DEAD TRACKS DETECTOR (Canciones No Disponibles) ===")
    
    # Obtener el mercado del usuario para mayor precisión
    user_info = sp.me()
    market = user_info.get('country', 'US')
    
    mode, pl_id = select_playlist(sp, "Elige una playlist para escanear", include_liked=True)
    if not mode: return

    print(f"⏳ Obteniendo canciones (Mercado: {market})...")
    tracks = get_all_tracks(sp, mode, pl_id, market=market)
    
    if not tracks:
        print("❌ No se encontraron canciones.")
        return

    dead_tracks = []
    
    print(f"🧬 Analizando {len(tracks)} canciones...")
    
    for i, item in enumerate(tracks):
        track = item.get('track')
        if not track: continue
        
        # Una canción puede no estar disponible si:
        # 1. No tiene 'is_playable' (si pedimos con mercado)
        # 2. Está marcada explícitamente como no disponible
        
        # Nota: 'is_playable' solo aparece si se pasa el parámetro 'market' en la petición
        playable = track.get('is_playable', True)
        
        if not playable:
            dead_tracks.append(track)
        
        # Progreso para la GUI
        if i % 10 == 0 or i == len(tracks) - 1:
            percent = int(((i + 1) / len(tracks)) * 100)
            print(f"PROG:{percent}")
            sys.stdout.flush()

    if not dead_tracks:
        print("\n✅ ¡Buenas noticias! Todas las canciones están disponibles.")
    else:
        print(f"\n⚠️ Se han encontrado {len(dead_tracks)} canciones no disponibles:")
        for t in dead_tracks:
            artists = ", ".join([a['name'] for a in t['artists']])
            print(f" - {t['name']} [{artists}]")
        
        print("\n¿Qué quieres hacer?")
        print("1: Eliminar estas canciones de la playlist")
        print("q: Solo listar y salir")
        
        choice = input("\nElige una opción: ").strip().lower()
        
        if choice == '1' and mode == 'playlist':
            print("⏳ Eliminando canciones...")
            uris_to_remove = [t['uri'] for t in dead_tracks]
            
            # Spotify permite eliminar hasta 100 de golpe
            for i in range(0, len(uris_to_remove), 100):
                batch = uris_to_remove[i:i+100]
                sp.playlist_remove_all_occurrences_of_items(pl_id, batch)
            
            print("✅ Canciones eliminadas con éxito.")
        elif choice == '1' and mode == 'liked':
            print("⏳ Quitando de 'Tus Me Gusta'...")
            ids_to_remove = [t['id'] for t in dead_tracks]
            for i in range(0, len(ids_to_remove), 50):
                batch = ids_to_remove[i:i+50]
                sp.current_user_saved_tracks_delete(batch)
            print("✅ Canciones quitadas de tus favoritos.")
        else:
            print("👋 Proceso finalizado sin cambios.")

if __name__ == "__main__":
    main()
