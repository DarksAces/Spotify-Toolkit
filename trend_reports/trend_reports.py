import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from collections import Counter
from tqdm import tqdm

# --- CONFIGURACIÓN Y AUTENTICACIÓN ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

try:
    from utils.auth import get_spotify_client
    from utils.helpers import get_all_tracks
    sp = get_spotify_client()
except ImportError:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope='user-library-read user-top-read'
    ))

def analyze_genres(tracks):
    print("🧬 Analizando géneros (esto puede tardar si hay muchos artistas)...")
    artist_ids = set()
    for t in tracks:
        for artist in t['track']['artists']:
            artist_ids.add(artist['id'])
    
    artist_ids = list(artist_ids)
    genres = []
    # Spotify limit for multiple artists is 50
    with tqdm(total=len(artist_ids), desc="Analizando artistas", unit="artist") as pbar:
        for i in range(0, len(artist_ids), 50):
            batch = artist_ids[i:i+50]
            batch = [aid for aid in batch if aid]
            if batch:
                artists_data = sp.artists(batch)['artists']
                for a in artists_data:
                    if a and 'genres' in a:
                        genres.extend(a['genres'])
                pbar.update(len(batch))
    
    return Counter(genres).most_common(10)

def save_report(top_genres, total_tracks):
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"Spotify_Trend_Report_{date_str}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("🎵 SPOTIFY TREND REPORT 🎵\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("="*30 + "\n\n")
        
        f.write(f"📊 Resumen de Biblioteca:\n")
        f.write(f"- Total de canciones analizadas: {total_tracks}\n\n")
        
        f.write("🧬 Top 10 Géneros:\n")
        for genre, count in top_genres:
            f.write(f"- {genre.title()}: {count} artistas\n")
        
        f.write("\n" + "="*30 + "\n")
        f.write("Generado por Spotify Toolkit\n")
    
    return filename

def main():
    print("\n=== GENERAR INFORME DE TENDENCIAS ===")
    print("Analizando tus 'Canciones Favoritas' (Liked Songs) para el informe...")
    
    tracks = get_all_tracks(sp, "liked_songs")
    if not tracks:
        print("⚠️ No tienes canciones guardadas para analizar.")
        return

    top_genres = analyze_genres(tracks)
    
    print("\n✅ Análisis completado.")
    filename = save_report(top_genres, len(tracks))
    
    print(f"\n📄 Informe guardado como: {filename}")
    print("Contenido resumido:")
    print(f"- Género principal: {top_genres[0][0].title() if top_genres else 'N/A'}")

if __name__ == "__main__":
    main()
