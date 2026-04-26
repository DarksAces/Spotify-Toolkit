import os
import spotipy
import sys
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import time
from tqdm import tqdm

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
        scope='user-library-read playlist-read-private'
    ))

def obtener_datos_artistas(tracks):
    """Extrae los nombres de los artistas de una lista de tracks."""
    nombres_artistas = []
    for item in tracks:
        if item and item.get('track') and item['track'].get('artists'):
            for artist in item['track']['artists']:
                nombres_artistas.append(artist['name'])
    return nombres_artistas

def main():
    while True:
        print("\n=== ARTIST EXTRACTOR (Estadísticas de Artistas) ===")
        mode, pl_id = select_playlist(sp, "Elige una playlist para analizar", include_liked=True)
        
        if not mode: break
        
        tracks = get_all_tracks(sp, mode, pl_id)
        if not tracks:
            print("❌ No se encontraron canciones.")
            continue

        nombres = obtener_datos_artistas(tracks)
        if not nombres:
            print("❌ No se encontraron artistas en esta lista.")
            continue
            
        conteo = Counter(nombres)
        top = conteo.most_common(10)
        
        print(f"\n📊 TOP 10 ARTISTAS:")
        for art, count in top:
            print(f"   ∟ {art}: {count} canciones")
        
        # Guardar en archivo
        file_id = pl_id if pl_id else "liked_songs"
        nombre_archivo = f"artistas_{file_id}.txt"
        
        try:
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write(f"Resumen de artistas para: {pl_id}\n")
                f.write("="*40 + "\n")
                f.write(f"Total de artistas únicos: {len(conteo)}\n")
                f.write("="*40 + "\n\n")
                for art, count in conteo.most_common():
                    f.write(f"{art}: {count}\n")
            print(f"\n✅ Lista completa guardada en: {nombre_archivo}")
        except Exception as e:
            print(f"❌ Error al guardar el archivo: {e}")

        otra = input("\n¿Quieres analizar otra playlist? (s/n): ").strip().lower()
        if otra != 's': break

if __name__ == "__main__":
    main()