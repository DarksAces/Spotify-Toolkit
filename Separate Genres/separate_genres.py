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

def get_common_genres(tracks):
    """Analiza la lista y devuelve los géneros más comunes."""
    artist_ids = set()
    for item in tracks:
        track = item['track']
        if track and track['artists']:
            artist_ids.add(track['artists'][0]['id'])
    
    genre_counts = {}
    artist_ids_list = list(artist_ids)
    
    print(f"📦 Analizando géneros de {len(artist_ids_list)} artistas...")
    for i in range(0, len(artist_ids_list), 50):
        batch = artist_ids_list[i:i+50]
        try:
            artists_data = sp.artists(batch)['artists']
            for artist in artists_data:
                if artist:
                    for g in artist['genres']:
                        genre_counts[g] = genre_counts.get(g, 0) + 1
        except: continue
            
    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_genres[:15]

def classify_tracks_by_genre(tracks, genres_to_classify):
    artist_ids = set()
    for item in tracks:
        track = item['track']
        if track and track['artists']:
            artist_ids.add(track['artists'][0]['id'])
    
    artist_genres = {}
    artist_ids_list = list(artist_ids)
    
    for i in range(0, len(artist_ids_list), 50):
        batch = artist_ids_list[i:i+50]
        while True:
            try:
                artists_data = sp.artists(batch)['artists']
                for artist in artists_data:
                    if artist:
                        artist_genres[artist['id']] = [g.lower() for g in artist['genres']]
                break
            except ReadTimeout:
                time.sleep(5)
            except SpotifyException as e:
                if e.http_status == 429:
                    time.sleep(int(e.headers.get('Retry-After', 1)))
                else: raise e

    genre_dict = {genre: [] for genre in genres_to_classify}
    for item in tracks:
        track = item['track']
        if not track or not track['artists']: continue
        
        artist_id = track['artists'][0]['id']
        genres = artist_genres.get(artist_id, [])

        for user_genre in genres_to_classify:
            for artist_genre in genres:
                if user_genre in artist_genre:
                    genre_dict[user_genre].append(track['id'])
                    break
            
    return genre_dict

def main():
    try:
        user_id = sp.me()['id']
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    mode, pl_id = select_playlist(sp, "SELECCIONA UNA LISTA PARA CLASIFICAR", include_liked=True)
    if not mode: return

    tracks = get_all_tracks(sp, mode, pl_id)
    if not tracks:
        print("❌ No se encontraron canciones.")
        return

    print("\n🔍 Analizando géneros sugeridos...")
    common = get_common_genres(tracks)
    if common:
        print("Géneros detectados:", ", ".join([f"{g[0]} ({g[1]})" for g in common]))
    
    print("\nIntroduce los géneros a clasificar (separados por comas):")
    genres_input = input("> ").split(',')
    genres_to_classify = [g.strip().lower() for g in genres_input if g.strip()]

    if not genres_to_classify:
        print("❌ No introdujiste géneros.")
        return

    classified = classify_tracks_by_genre(tracks, genres_to_classify)
    
    for genre, ids in classified.items():
        if ids:
            unique_ids = list(dict.fromkeys(ids))
            name = f"{genre.capitalize()} Mix"
            print(f"🛠️ Creando playlist: {name}")
            new_pl = sp.user_playlist_create(user_id, name, public=False)
            for i in range(0, len(unique_ids), 100):
                sp.playlist_add_items(new_pl['id'], unique_ids[i:i+100])
        else:
            print(f"⚠️ Sin canciones para: {genre}")

    print("\n✨ Proceso completado.")

if __name__ == "__main__":
    main()
