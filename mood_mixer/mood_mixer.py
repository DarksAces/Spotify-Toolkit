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
    print("\n=== MOOD MIXER (Mezcla por Ánimo) ===")
    mode, pl_id = select_playlist(sp, "Elige una playlist para filtrar", include_liked=True)
    if not mode: return

    tracks = get_all_tracks(sp, mode, pl_id)
    if not tracks: return

    print("\n¿Qué ambiente buscas?")
    print("1: Energético (High Energy)")
    print("2: Relajado (Chill/Acoustic)")
    print("3: Bailable (Danceable)")
    print("4: Feliz (Positive Vibes)")
    print("q: Cancelar")

    choice = input("\nElige una opción: ").strip().lower()
    if choice == 'q': return

    mood_filters = {
        "1": {"energy": (0.7, 1.0)},
        "2": {"energy": (0.0, 0.4), "acousticness": (0.5, 1.0)},
        "3": {"danceability": (0.7, 1.0)},
        "4": {"valence": (0.7, 1.0)}
    }
    
    selected_filter = mood_filters.get(choice)
    if not selected_filter:
        print("❌ Opción no válida.")
        return

    print("\n🧬 Analizando características de las canciones...")
    uris = [t['track']['uri'] for t in tracks if t['track'] and t['track'].get('uri')]
    filtered_uris = []
    
    total_uris = len(uris)
    with tqdm(total=total_uris, desc="Analizando audio", unit="track") as pbar:
        for i in range(0, total_uris, 100):
            batch = uris[i:i+100]
            try:
                features = sp.audio_features(batch)
                for feat in features:
                    if not feat: continue
                    match = True
                    for key, (vmin, vmax) in selected_filter.items():
                        val = feat.get(key, 0)
                        if not (vmin <= val <= vmax):
                            match = False
                            break
                    if match:
                        filtered_uris.append(feat['uri'])
            except Exception as e:
                print(f"\n⚠️ Error al obtener características: {e}")
                
            pbar.update(len(batch))
            # Progreso para la GUI
            percent = int(((i + len(batch)) / total_uris) * 100)
            print(f"PROG:{min(percent, 100)}")
            sys.stdout.flush()

    if not filtered_uris:
        print("\n⚠️ No se encontraron canciones que coincidan con ese ánimo.")
        return

    print(f"\n✅ Encontradas {len(filtered_uris)} canciones.")
    new_name = input("Nombre para la nueva playlist: ").strip()
    if not new_name: new_name = "Mood Mix"

    print("\n📤 Creando nueva playlist en Spotify...")
    user_id = sp.me()['id']
    new_pl = sp.user_playlist_create(user_id, new_name, public=False)
    
    total_filtered = len(filtered_uris)
    with tqdm(total=total_filtered, desc="Creando playlist", unit="track") as pbar:
        for i in range(0, total_filtered, 100):
            batch = filtered_uris[i:i+100]
            sp.playlist_add_items(new_pl['id'], batch)
            pbar.update(len(batch))
            
    print(f"\n✅ ¡Hecho! Playlist '{new_name}' creada.")

if __name__ == "__main__":
    main()
