import os
import random
import spotipy
import sys
from spotipy.oauth2 import SpotifyOAuth

# --- CONFIGURACIÓN Y AUTENTICACIÓN ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

try:
    from utils.auth import get_spotify_client
    from utils.helpers import select_playlist
    sp = get_spotify_client()
except ImportError:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope='playlist-read-private playlist-modify-public playlist-modify-private'
    ))

def mezclar_flexible(tracks, max_intentos=5000):
    print(f"🎲 Iniciando Smart Shuffle para {len(tracks)} canciones...")
    if len(tracks) < 2: return tracks

    mejor_mezcla = list(tracks)
    min_colisiones = len(tracks)

    for intento in range(max_intentos):
        random.shuffle(tracks)
        colisiones = 0
        for i in range(1, len(tracks)):
            if tracks[i]['artist'] == tracks[i-1]['artist'] or tracks[i]['album'] == tracks[i-1]['album']:
                colisiones += 1
        
        if colisiones == 0:
            print(f"   ∟ Mezcla perfecta encontrada en intento {intento+1}!")
            return tracks
        
        if colisiones < min_colisiones:
            min_colisiones = colisiones
            mejor_mezcla = list(tracks)
            
    print(f"   ⚠️ No se encontró una mezcla perfecta. Usando la mejor (colisiones: {min_colisiones})")
    return mejor_mezcla

def main():
    while True:
        print("\n=== SMART SHUFFLE (Mezcla inteligente) ===")
        pl = select_playlist(sp, "Elige la playlist para mezclar")
        
        if not pl: break
        
        canciones = []
        offset = 0
        print(f"🔍 Cargando canciones de '{pl['name']}'...")
        while True:
            res = sp.playlist_items(pl['id'], offset=offset, fields="items.track(uri,artists,album(name)),next")
            for item in res['items']:
                track = item['track']
                if track and track['uri'] and track['artists']:
                    canciones.append({
                        "uri": track['uri'],
                        "artist": track['artists'][0]['name'],
                        "album": track['album']['name']
                    })
            if not res['next']: break
            offset += len(res['items'])
            print(f"   ∟ Obtenidas {len(canciones)} canciones...")
        
        if not canciones:
            print("❌ La playlist está vacía.")
            continue

        mezcladas = mezclar_flexible(canciones)
        
        print("📤 Actualizando playlist en Spotify...")
        # Usamos replace_items porque es más eficiente para limpiar y rellenar
        uris = [t['uri'] for t in mezcladas]
        
        # Spotify permite añadir hasta 100 de golpe. Replace_items también.
        sp.playlist_replace_items(pl['id'], uris[:100])
        for i in range(100, len(uris), 100):
            sp.playlist_add_items(pl['id'], uris[i:i+100])
        
        print(f"✅ ¡Hecho! '{pl['name']}' ha sido mezclada.")
        
        otra = input("\n¿Quieres mezclar otra playlist? (s/n): ").strip().lower()
        if otra != 's': break

if __name__ == "__main__":
    main()
