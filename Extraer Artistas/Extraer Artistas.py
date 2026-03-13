import os
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from collections import Counter
import time

# Autenticación (Permisos de lectura)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope='user-library-read playlist-read-private playlist-read-collaborative'
))

def get_user_playlists():
    print("🔍 Cargando tus playlists...")
    results = sp.current_user_playlists()
    playlists = results['items']
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])
    return playlists

def obtener_datos_playlist(playlist_id, playlist_name):
    print(f"\n[INFO] Procesando playlist: {playlist_name} ⏳")
    
    todos_los_artistas_nombres = []
    artista_a_id = {}
    
    offset = 0
    while True:
        resultados = sp.playlist_tracks(playlist_id, offset=offset)
        tracks = resultados['items']
        print(f"   ∟ Obtenidas {len(tracks) + offset} canciones...")
        
        for item in tracks:
            if item and item.get('track') and item['track'].get('artists'):
                for artist in item['track']['artists']:
                    artist_name = artist['name']
                    todos_los_artistas_nombres.append(artist_name)
                    if artist_name not in artista_a_id:
                        artista_a_id[artist_name] = artist['id']
        
        if not resultados['next']: break
        offset += len(tracks)
    
    return todos_los_artistas_nombres, artista_a_id

def main():
    playlists = get_user_playlists()
    
    while True:
        print("\n=== SELECTOR DE PLAYLIST (Extraer Artistas y Géneros) ===")
        for i, pl in enumerate(playlists, start=1):
            print(f"{i}: {pl['name']} ({pl['tracks']['total']} canciones)")
        
        choice = input("\nElige el número de la lista para analizar (o 'q' para salir): ").strip()
        if choice.lower() == 'q': break
        if not choice.isdigit(): continue
        
        idx = int(choice)
        if 1 <= idx <= len(playlists):
            pl = playlists[idx - 1]
            nombres, mapeo_id = obtener_datos_playlist(pl['id'], pl['name'])
            
            conteo = Counter(nombres)
            top = conteo.most_common(10)
            
            print(f"\n📊 TOP 10 ARTISTAS EN '{pl['name']}':")
            for art, count in top:
                print(f"   ∟ {art}: {count} veces")
            
            # Guardar en archivo
            nombre_archivo = f"artistas_{pl['name'].replace(' ', '_')}.txt"
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write(f"Resumen de artistas para: {pl['name']}\n")
                f.write("="*30 + "\n")
                for art, count in conteo.most_common():
                    f.write(f"{art}: {count}\n")
            
            print(f"\n✅ Lista completa guardada en: {nombre_archivo}")
        else:
            print("❌ Número fuera de rango.")

        otra = input("\n¿Quieres analizar otra playlist? (s/n): ").strip().lower()
        if otra != 's': break

if __name__ == "__main__":
    main()