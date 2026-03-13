import time
import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from requests.exceptions import ReadTimeout
from spotipy.exceptions import SpotifyException

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
        scope='user-library-read playlist-read-private playlist-modify-public playlist-modify-private'
    ))

def classify_tracks_by_artist(tracks):
    artist_dict = {}
    for item in tracks:
        track = item['track']
        if track and track['artists']:
            artist_name = track['artists'][0]['name']
            artist_dict.setdefault(artist_name, []).append(track['id'])
    return artist_dict

def classify_tracks_by_similar_artists(tracks):
    similar_artist_dict = {}
    total = len(tracks)
    print(f"\nAnalizando artistas similares para {total} canciones...")
    
    # Cache para no repetir búsquedas de artistas relacionados
    related_cache = {}

    for idx, item in enumerate(tracks, 1):
        track = item['track']
        if not track or not track['artists']: continue
        
        artist = track['artists'][0]
        artist_id = artist['id']
        artist_name = artist['name']

        if idx % 10 == 0 or idx == total:
            print(f"   ∟ Procesando {idx}/{total}...")

        if artist_id not in related_cache:
            while True:
                try:
                    related = sp.artist_related_artists(artist_id)['artists']
                    related_cache[artist_id] = [r['name'] for r in related]
                    break
                except ReadTimeout:
                    time.sleep(2)
                except SpotifyException as e:
                    if e.http_status == 429:
                        time.sleep(int(e.headers.get('Retry-After', 1)))
                    else: raise e

        for related_name in related_cache[artist_id]:
            similar_artist_dict.setdefault(related_name, []).append(track['id'])

    return similar_artist_dict

def main():
    try:
        user_id = sp.me()['id']
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    mode, pl_id = select_playlist(sp, "SELECCIONA UNA LISTA PARA SEPARAR", include_liked=True)
    if not mode: return

    tracks = get_all_tracks(sp, mode, pl_id)
    if not tracks: return

    print("\n¿Quieres agrupar por artista principal (A) o por artistas similares (S)?")
    choice = input("Selecciona (A/S): ").strip().lower()

    if choice == 'a':
        classified = classify_tracks_by_artist(tracks)
    elif choice == 's':
        classified = classify_tracks_by_similar_artists(tracks)
    else:
        print("❌ Opción inválida.")
        return

    # Mostrar resumen
    print(f"\nSe han detectado {len(classified)} grupos.")
    print("Creando playlists para grupos con más de 3 canciones...")

    for artist, ids in classified.items():
        if len(ids) >= 3:
            unique_ids = list(dict.fromkeys(ids))
            name = f"{artist} Mix"
            print(f"   ∟ Creando: {name} ({len(unique_ids)} tracks)")
            new_pl = sp.user_playlist_create(user_id, name, public=False)
            for i in range(0, len(unique_ids), 100):
                sp.playlist_add_items(new_pl['id'], unique_ids[i:i+100])

    print("\n✨ Proceso completado.")

if __name__ == "__main__":
    main()
