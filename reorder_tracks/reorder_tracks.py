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

def reorder_by_artist(tracks, pl_id):
    artist_target = input("\n🎤 Artista que quieres mover al final: ").lower().strip()
    matches = []
    for i, item in enumerate(tracks):
        if not item['track']: continue
        track_artists = [a['name'].lower().strip() for a in item['track']['artists']]
        if any(artist_target in a for a in track_artists):
            matches.append(i)

    if not matches:
        print(f"⚠️ No se encontraron canciones de '{artist_target}'.")
        return

    print(f"📤 Moviendo {len(matches)} canciones al final...")
    total_tracks = len(tracks)
    for idx in sorted(matches, reverse=True):
        sp.playlist_reorder_items(pl_id, range_start=idx, insert_before=total_tracks)
    print(f"✅ ¡Hecho! Artista movido al final.")

def get_audio_features_in_batches(track_ids):
    features = []
    for i in range(0, len(track_ids), 100):
        batch = [tid for tid in track_ids[i:i+100] if tid]
        if batch:
            features.extend(sp.audio_features(batch))
    return features

def sort_by_bpm(tracks, pl_id):
    print("\n⏳ Obteniendo datos de BPM...")
    track_ids = [t['track']['id'] for t in tracks if t['track']]
    features = get_audio_features_in_batches(track_ids)
    
    # Mapear BPM a tracks
    track_data = []
    for t, f in zip(tracks, features):
        if f:
            track_data.append({
                'uri': t['track']['uri'],
                'bpm': f['tempo'],
                'name': t['track']['name']
            })
    
    print("\n¿Cómo quieres ordenar?")
    print("1: BPM Ascendente (Lento -> Rápido)")
    print("2: BPM Descendente (Rápido -> Lento)")
    order_choice = input("Elige (1-2): ").strip()
    
    reverse = True if order_choice == '2' else False
    sorted_tracks = sorted(track_data, key=lambda x: x['bpm'], reverse=reverse)
    
    print(f"📤 Actualizando playlist con el nuevo orden...")
    new_uris = [t['uri'] for t in sorted_tracks]
    
    # Reemplazar canciones en la playlist (max 100 por vez)
    # Primero reemplazamos las primeras 100 (esto borra el resto)
    sp.playlist_replace_items(pl_id, new_uris[:100])
    # Luego añadimos el resto si hay
    if len(new_uris) > 100:
        for i in range(100, len(new_uris), 100):
            sp.playlist_add_items(pl_id, new_uris[i:i+100])
            
    print(f"✅ ¡Playlist ordenada exitosamente por BPM!")

def main():
    while True:
        print("\n=== ORGANIZAR LISTAS (BPM / Artistas) ===")
        mode, pl_id = select_playlist(sp, "SELECCIONA UNA LISTA", include_liked=True)
        
        if not mode: break
        if mode == "liked_songs":
            print("⚠️ No se puede reordenar 'Favoritos' directamente.")
            print("Crea una playlist nueva a partir de tus favoritos primero.")
            continue

        tracks = get_all_tracks(sp, mode, pl_id)
        if not tracks: continue

        print("\n¿Qué quieres hacer?")
        print("1: Mover un artista al final")
        print("2: Ordenar toda la lista por BPM")
        print("q: Volver")
        
        choice = input("\nElige una opción: ").strip().lower()
        
        if choice == '1':
            reorder_by_artist(tracks, pl_id)
        elif choice == '2':
            sort_by_bpm(tracks, pl_id)
        elif choice == 'q':
            break
        else:
            print("❌ Opción no válida.")

        otra = input("\n¿Quieres hacer algo más con esta u otra lista? (s/n): ").strip().lower()
        if otra != 's': break

if __name__ == "__main__":
    main()
