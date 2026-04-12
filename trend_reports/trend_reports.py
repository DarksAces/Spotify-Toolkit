import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from collections import Counter

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

def get_audio_features_in_batches(track_ids):
    features = []
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i+100]
        # Filter out None IDs
        batch = [tid for tid in batch if tid]
        if batch:
            features.extend(sp.audio_features(batch))
    return features

def analyze_genres(tracks):
    print("🧬 Analizando géneros (esto puede tardar si hay muchos artistas)...")
    artist_ids = set()
    for t in tracks:
        for artist in t['track']['artists']:
            artist_ids.add(artist['id'])
    
    artist_ids = list(artist_ids)
    genres = []
    # Spotify limit for multiple artists is 50
    for i in range(0, len(artist_ids), 50):
        batch = artist_ids[i:i+50]
        batch = [aid for aid in batch if aid]
        if batch:
            artists_data = sp.artists(batch)['artists']
            for a in artists_data:
                if a and 'genres' in a:
                    genres.extend(a['genres'])
    
    return Counter(genres).most_common(10)

def calculate_audio_profile(features):
    print("📈 Calculando perfil de audio...")
    valid_features = [f for f in features if f]
    if not valid_features:
        return None
    
    count = len(valid_features)
    avg_energy = sum(f['energy'] for f in valid_features) / count
    avg_valence = sum(f['valence'] for f in valid_features) / count
    avg_danceability = sum(f['danceability'] for f in valid_features) / count
    avg_tempo = sum(f['tempo'] for f in valid_features) / count
    
    return {
        "energy": avg_energy,
        "valence": avg_valence,
        "danceability": avg_danceability,
        "tempo": avg_tempo
    }

def save_report(top_genres, profile, total_tracks):
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
        f.write("\n")
        
        if profile:
            f.write("📈 Perfil de Audio Promedio:\n")
            f.write(f"- Energía: {profile['energy']:.2f} (0-1)\n")
            f.write(f"- Positividad (Valence): {profile['valence']:.2f} (0-1)\n")
            f.write(f"- Bailabilidad: {profile['danceability']:.2f} (0-1)\n")
            f.write(f"- Ritmo (BPM): {profile['tempo']:.1f} BPM\n")
        
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
    
    track_ids = [t['track']['id'] for t in tracks]
    features = get_audio_features_in_batches(track_ids)
    profile = calculate_audio_profile(features)
    
    print("\n✅ Análisis completado.")
    filename = save_report(top_genres, profile, len(tracks))
    
    print(f"\n📄 Informe guardado como: {filename}")
    print("Contenido resumido:")
    print(f"- Género principal: {top_genres[0][0].title() if top_genres else 'N/A'}")
    if profile:
        print(f"- BPM Promedio: {profile['tempo']:.1f}")

if __name__ == "__main__":
    main()
