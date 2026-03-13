import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
import sys
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope='playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'
))

# Función para obtener top tracks con paginación (máx 50 por request)
def get_top_tracks(time_range="medium_term", max_tracks=50):
    results = []
    print("🔍 Obteniendo tus canciones favoritas...")
    while len(results) < max_tracks:
        batch_size = min(50, max_tracks - len(results))  # límite máximo 50
        batch = sp.current_user_top_tracks(time_range=time_range, limit=batch_size, offset=offset)
        results.extend(batch['items'])
        print(f"   ∟ Obtenidas {len(results)} canciones...")
        if len(batch['items']) < batch_size:
            break
        offset += batch_size
    return results

# Menú de opciones accesibles
print("Elige rango temporal:")
print("1: Últimas 4 semanas")
print("2: Últimos 6 meses")
print("3: Todo el tiempo")

opcion = input("Tu opción: ")

if opcion not in ["1", "2", "3"]:
    print("Opción no válida. Solo se pueden seleccionar rangos accesibles por la API.")
    sys.sys.exit()

time_range = {"1": "short_term", "2": "medium_term", "3": "long_term"}[opcion]

# Obtener top tracks (máximo 50 por defecto)
top_tracks = get_top_tracks(time_range=time_range, max_tracks=50)

# Mostrar resultados
print(f"\nTop canciones ({time_range}):\n")
for i, t in enumerate(top_tracks, start=1):
    artistas = ", ".join([a['name'] for a in t['artists']])
    release_date = t['album']['release_date']
    print(f"{i}. {t['name']} - {artistas} ({release_date})")

