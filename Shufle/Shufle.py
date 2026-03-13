import os
import random
import spotipy
import sys
from spotipy.oauth2 import SpotifyOAuth

# Autenticación
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope='user-library-read playlist-read-private playlist-modify-public playlist-modify-private'
))

def get_user_playlists():
    print("🔍 Cargando tus playlists...")
    results = sp.current_user_playlists()
    playlists = results['items']
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])
    return playlists

def mezclar_flexible(tracks, max_intentos=5000):
    print(f"🎲 Iniciando Smart Shuffle para {len(tracks)} canciones...")
    for intento in range(max_intentos):
        random.shuffle(tracks)
        valido = True
        for i in range(1, len(tracks)):
            prev = tracks[i-1]
            curr = tracks[i]
            if curr['artist'] == prev['artist'] or curr['album'] == prev['album']:
                valido = False
                break
        if valido:
            print(f"   ∟ Mezcla perfecta encontrada en intento {intento+1}")
            return tracks
    return tracks

def main():
    playlists = get_user_playlists()
    
    while True:
        print("\n=== SMART SHUFFLE (Mezcla inteligente) ===")
        for i, pl in enumerate(playlists, start=1):
            print(f"{i}: {pl['name']} ({pl['tracks']['total']} canciones)")
        
        choice = input("\nElige el número de la lista para mezclar (o 'q' para salir): ").strip()
        if choice.lower() == 'q': break
        if not choice.isdigit(): continue
        
        idx = int(choice)
        if 1 <= idx <= len(playlists):
            pl = playlists[idx - 1]
            pl_id = pl['id']
            
            # Obtener canciones
            canciones = []
            offset = 0
            print(f"🔍 Cargando canciones de '{pl['name']}'...")
            while True:
                res = sp.playlist_items(pl_id, offset=offset, fields="items.track(uri,name,artists,album(name)),next")
                for item in res['items']:
                    track = item['track']
                    if track:
                        canciones.append({
                            "uri": track['uri'],
                            "artist": track['artists'][0]['name'],
                            "album": track['album']['name']
                        })
                print(f"   ∟ Obtenidas {len(canciones)} canciones...")
                if not res['next']: break
                offset += len(res['items'])
            
            # Mezclar
            mezcladas = mezclar_flexible(canciones)
            
            # Aplicar a la playlist
            print("📤 Actualizando playlist en Spotify...")
            sp.playlist_replace_items(pl_id, [])
            for i in range(0, len(mezcladas), 100):
                sp.playlist_add_items(pl_id, [t['uri'] for t in mezcladas[i:i+100]])
            
            print(f"✅ ¡Hecho! '{pl['name']}' ha sido mezclada con éxito.")
        else:
            print("❌ Número fuera de rango.")

        otra = input("\n¿Quieres mezclar otra playlist? (s/n): ").strip().lower()
        if otra != 's': break

if __name__ == "__main__":
    main()
