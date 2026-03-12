import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyOauthError

# ------------------- AUTENTICACIÓN -------------------
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope=["playlist-modify-public", "playlist-modify-private"]
))
    
    
except SpotifyOauthError as e:
    print(f"\n❌ Error de autenticación: {e}")
    print("Revisa tus credenciales o variables de entorno (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI).")
    exit()

# ------------------- SELECCIÓN DE FUENTE -------------------
print("\n¿De dónde quieres mover las canciones?")
print("1️⃣  Una playlist")
print("2️⃣  Tus canciones favoritas (Liked Songs)")

choice = input("\nElige una opción (1 o 2): ").strip()

if choice == "2":
    source = "liked"
    print("\nObteniendo tus canciones favoritas...")
    tracks = []
    offset = 0
    while True:
        results = sp.current_user_saved_tracks(limit=50, offset=offset)
        tracks.extend(results['items'])
        if len(results['items']) < 50:
            break
        offset += 50
    playlist_name = "Tus canciones favoritas ❤️"
    playlist_id = None
else:
    source = "playlist"
    # ------------------- LISTAR PLAYLISTS -------------------
    playlists = sp.current_user_playlists(limit=50)['items']
    if not playlists:
        print("❌ No se encontraron playlists en tu cuenta.")
        exit()

    print("\n🎧 Tus playlists:")
    for i, p in enumerate(playlists, 1):
        print(f"{i}. {p['name']} → {p['id']}")

    try:
        playlist_idx = int(input("\nElige el número de la playlist donde quieres mover canciones: ")) - 1
        playlist_id = playlists[playlist_idx]['id']
        playlist_name = playlists[playlist_idx]['name']
    except (ValueError, IndexError):
        print("❌ Selección inválida.")
        exit()

    # ------------------- OBTENER TRACKS -------------------
    print(f"\nObteniendo canciones de '{playlist_name}'...")
    tracks = []
    offset = 0
    while True:
        response = sp.playlist_tracks(playlist_id, limit=100, offset=offset)
        tracks.extend(response['items'])
        if len(response['items']) < 100:
            break
        offset += 100

# ------------------- FILTRAR POR ARTISTA -------------------
artist_name_input = input("\n🎤 Escribe el nombre del artista que quieres mover al final: ").lower().strip()

indices = []
for i, t in enumerate(tracks):
    track_artists = [a['name'].lower().strip() for a in t['track']['artists']]
    if any(artist_name_input in a for a in track_artists):
        indices.append(i)

if not indices:
    print(f"⚠️ No se encontraron canciones de '{artist_name_input}' en '{playlist_name}'.")
    exit()

# ------------------- REORDENAR (solo si es playlist) -------------------
if source == "liked":
    print("⚠️ No puedes reordenar directamente las canciones de tus favoritos (limitación de Spotify API).")
    print("Puedes crear una nueva playlist con esas canciones si lo deseas.")
    create = input("\n¿Quieres crear una nueva playlist con esas canciones? (s/n): ").strip().lower()
    if create == "s":
        user_id = sp.me()['id']
        new_playlist = sp.user_playlist_create(user_id, f"{artist_name_input.capitalize()} - Desde tus favoritos")
        track_ids = [t['track']['id'] for i, t in enumerate(tracks) if i in indices and t['track']['id']]
        for i in range(0, len(track_ids), 100):
            sp.playlist_add_items(new_playlist['id'], track_ids[i:i+100])
        print(f"\n✅ Nueva playlist creada: {artist_name_input.capitalize()} - Desde tus favoritos")
    else:
        print("\n👌 No se realizó ningún cambio.")
else:
    for idx in reversed(indices):
        sp.playlist_reorder_items(playlist_id, range_start=idx, insert_before=len(tracks))
        tracks.append(tracks.pop(idx))
    print(f"\n✅ Todas las canciones de '{artist_name_input}' se han movido al final de la playlist '{playlist_name}'.")

print("\n🎶 Proceso completado con éxito.")
