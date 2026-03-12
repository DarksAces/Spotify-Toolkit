import time
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from requests.exceptions import ReadTimeout
from spotipy.exceptions import SpotifyException

# ===============================
# 🔐 AUTENTICACIÓN SPOTIFY
# ===============================
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope='user-library-read playlist-read-private playlist-modify-private playlist-modify-public'
))

# ===============================
# 🎧 OBTENER CANCIONES FAVORITAS
# ===============================
def get_liked_songs():
    print("Obteniendo tus canciones favoritas ❤️...")
    results = sp.current_user_saved_tracks(limit=50)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    print(f"Total de canciones obtenidas: {len(tracks)}")
    return tracks

# ===============================
# 📜 OBTENER PLAYLISTS DEL USUARIO
# ===============================
def get_user_playlists():
    print("Cargando tus playlists...")
    results = sp.current_user_playlists()
    playlists = results['items']
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])
    print(f"Playlists encontradas: {len(playlists)}")
    return playlists

# ===============================
# 🎯 SELECCIONAR PLAYLIST O FAVORITOS
# ===============================
def choose_source(playlists):
    print("\n=== SELECCIONA UNA LISTA ===")
    print("0: ❤️ Tus canciones favoritas (Liked Songs)")
    for idx, playlist in enumerate(playlists, start=1):
        print(f"{idx}: {playlist['name']}")

    choice = input("Número de lista: ").strip()
    if not choice.isdigit():
        print("❌ Selección inválida.")
        return None, None

    choice = int(choice)
    if choice == 0:
        print("Has elegido tus canciones favoritas ❤️")
        return "liked_songs", None
    elif 1 <= choice <= len(playlists):
        playlist = playlists[choice - 1]
        print(f"Has elegido: {playlist['name']}")
        return "playlist", playlist['id']
    else:
        print("❌ Número fuera de rango.")
        return None, None

# ===============================
# 🎵 OBTENER CANCIONES DE UNA PLAYLIST
# ===============================
def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    print(f"Total de canciones en la playlist: {len(tracks)}")
    return tracks

# ===============================
# 🧩 CLASIFICAR POR ARTISTA
# ===============================
def classify_tracks_by_artist(tracks):
    artist_dict = {}
    for item in tracks:
        track = item['track']
        artist_name = track['artists'][0]['name']
        artist_dict.setdefault(artist_name, []).append(track['id'])
    return artist_dict

# ===============================
# 🎯 CLASIFICAR POR ARTISTAS SIMILARES
# ===============================
def classify_tracks_by_similar_artists(tracks):
    similar_artist_dict = {}
    for item in tracks:
        track = item['track']
        artist = track['artists'][0]
        artist_id = artist['id']
        artist_name = artist['name']

        while True:
            try:
                related_artists = sp.artist_related_artists(artist_id)['artists']
                break
            except ReadTimeout:
                print(f"⏳ Timeout obteniendo artistas relacionados de {artist_name}. Reintentando...")
                time.sleep(5)
            except SpotifyException as e:
                if e.http_status == 429:
                    retry_after = int(e.headers.get('Retry-After', 1))
                    print(f"🚦 Rate limit alcanzado. Esperando {retry_after}s...")
                    time.sleep(retry_after)
                else:
                    raise e

        for related in related_artists:
            similar_artist_dict.setdefault(related['name'], []).append(track['id'])

        time.sleep(0.1)
    return similar_artist_dict

# ===============================
# 🧱 CREAR PLAYLISTS NUEVAS
# ===============================
def create_playlist(user_id, name, track_ids):
    print(f"🛠️ Creando playlist: {name}")
    new_playlist = sp.user_playlist_create(user_id, name, public=False)
    for i in range(0, len(track_ids), 100):
        sp.playlist_add_items(new_playlist['id'], track_ids[i:i+100])
    print(f"✅ Playlist creada: {name} ({len(track_ids)} canciones)")
    return new_playlist['id']

# ===============================
# 🚀 MAIN
# ===============================
if __name__ == "__main__":
    user_id = sp.me()['id']
    playlists = get_user_playlists()

    mode, playlist_id = choose_source(playlists)
    if not mode:
        exit()

    if mode == "liked_songs":
        tracks = get_liked_songs()
    else:
        tracks = get_playlist_tracks(playlist_id)

    if not tracks:
        print("❌ No se encontraron canciones.")
        exit()

    print("\n¿Quieres agrupar por artista (A) o por artistas similares (S)?")
    choice = input("Selecciona (A/S): ").strip().lower()

    if choice == 'a':
        classified = classify_tracks_by_artist(tracks)
        print("🎶 Clasificando por artista principal...")
    elif choice == 's':
        classified = classify_tracks_by_similar_artists(tracks)
        print("🎵 Clasificando por artistas similares...")
    else:
        print("❌ Opción inválida.")
        exit()

    for artist, ids in classified.items():
        if ids:
            create_playlist(user_id, f"{artist} - {('Favoritos' if mode == 'liked_songs' else 'Subset')}", ids)
        else:
            print(f"Sin canciones para {artist}.")

    print("\n✨ Proceso completado con éxito.")
