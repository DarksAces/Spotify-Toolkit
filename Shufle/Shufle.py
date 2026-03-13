import os
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Autenticación
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope='user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'
    ))
# Pedir la playlist
playlist_url = input("Ingresa el URL o ID de la playlist que quieres mezclar: ")
playlist_id = playlist_url.split("/")[-1].split("?")[0]

# Obtener canciones
print("🔍 Obteniendo canciones de la playlist...")
canciones = []
offset = 0
while True:
    response = sp.playlist_items(
        playlist_id, 
        offset=offset, 
        fields="items.track(uri,name,artists,album(name,release_date),duration_ms,popularity),next"
    )
    if not response['items']:
        break
    for item in response['items']:
        track = item['track']
        if track:
            release_year = track['album']['release_date'].split("-")[0] if track['album']['release_date'] else None
            canciones.append({
                "uri": track['uri'],
                "artist": track['artists'][0]['name'],
                "album": track['album']['name'],
                "name": track['name'],
                "duration_ms": track['duration_ms'],
                "popularity": track['popularity'],
                "year": release_year
            })
    
    print(f"   ∟ Obtenidas {len(canciones)} canciones...")
    
    if not response['next']:
        break
    offset += len(response['items'])

print(f"Se encontraron {len(canciones)} canciones.")

# Función de mezcla flexible
def mezclar_flexible(tracks, max_intentos=5000):
    for intento in range(max_intentos):
        random.shuffle(tracks)
        valido = True
        for i in range(1, len(tracks)):
            prev = tracks[i-1]
            curr = tracks[i]

            # Restricciones fuertes: artista y álbum consecutivo
            if curr['artist'] == prev['artist'] or curr['album'] == prev['album']:
                valido = False
                break
            
            # Restricciones suaves: año, duración, popularidad, palabras
            # Solo se aplican si no bloquean la mezcla
            # Año consecutivo
            if curr['year'] and prev['year'] and curr['year'] == prev['year']:
                if random.random() < 0.8:  # 80% de intentar cumplir
                    valido = False
                    break
            
            # Duración similar
            if abs(curr['duration_ms'] - prev['duration_ms']) / prev['duration_ms'] < 0.1:
                if random.random() < 0.5:  # 50% de intentar cumplir
                    valido = False
                    break
            
            # Popularidad similar
            if abs(curr['popularity'] - prev['popularity']) < 10:
                if random.random() < 0.5:
                    valido = False
                    break
            
            # Palabras repetidas
            prev_words = set(prev['name'].lower().split())
            curr_words = set(curr['name'].lower().split())
            if prev_words & curr_words:
                if random.random() < 0.5:
                    valido = False
                    break

        if valido:
            print(f"Mezcla válida encontrada en intento {intento+1}")
            return tracks

    print("⚠️ No se pudo cumplir todas las restricciones estrictas, devolviendo mezcla parcial.")
    return tracks

# Mezclar
canciones_mezcladas = mezclar_flexible(canciones)

# Vaciar playlist y añadir canciones en bloques de 100
sp.playlist_replace_items(playlist_id, [])
for i in range(0, len(canciones_mezcladas), 100):
    sp.playlist_add_items(playlist_id, [t['uri'] for t in canciones_mezcladas[i:i+100]])

print(f"✅ Playlist mezclada con {len(canciones_mezcladas)} canciones con mezcla flexible.")
