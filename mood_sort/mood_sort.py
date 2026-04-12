import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

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
        scope='user-library-read playlist-read-private playlist-modify-public playlist-modify-private'
    ))

def get_audio_features_in_batches(track_ids):
    features = []
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i+100]
        features.extend(sp.audio_features(batch))
    return features

def classify_tracks(tracks, features):
    categories = {
        "Uplifting": [],
        "Melancholic": [],
        "Deep Focus": []
    }
    
    for track, feat in zip(tracks, features):
        if not feat: continue
        
        valence = feat['valence']
        energy = feat['energy']
        instr = feat['instrumentalness']
        
        # Uplifting: High Valence, High Energy
        if valence > 0.7 and energy > 0.7:
            categories["Uplifting"].append(track)
        
        # Melancholic: Low Valence, Low Energy
        elif valence < 0.35 and energy < 0.4:
            categories["Melancholic"].append(track)
            
        # Deep Focus: Med/Low Valence, Low Energy, High Instrumentalness
        elif 0.2 < valence < 0.5 and energy < 0.4 and instr > 0.5:
            categories["Deep Focus"].append(track)
            
    return categories

def create_mood_playlists(categories, original_name):
    user_id = sp.current_user()['id']
    for mood, playlist_tracks in categories.items():
        if not playlist_tracks:
            print(f"ℹ️ No se encontraron canciones para el mood: {mood}")
            continue
            
        print(f"🎵 Creando playlist para {mood} ({len(playlist_tracks)} canciones)...")
        new_name = f"{original_name} - {mood}"
        new_pl = sp.user_playlist_create(user_id, new_name, public=False)
        
        track_uris = [t['track']['uri'] for t in playlist_tracks]
        # Añadir canciones en batches de 100
        for i in range(0, len(track_uris), 100):
            sp.playlist_add_items(new_pl['id'], track_uris[i:i+100])
        
        print(f"✅ ¡Playlist '{new_name}' creada con éxito!")

def main():
    print("\n=== CLASIFICACIÓN POR MOOD (Valence & Energy) ===")
    mode, pl_id = select_playlist(sp, "SELECCIONA UNA LISTA PARA ANALIZAR", include_liked=True)
    if not mode: return

    tracks = get_all_tracks(sp, mode, pl_id)
    if not tracks:
        print("⚠️ No hay canciones para analizar.")
        return

    print("🔍 Obteniendo características de audio...")
    track_ids = [t['track']['id'] for t in tracks]
    features = get_audio_features_in_batches(track_ids)
    
    categories = classify_tracks(tracks, features)
    
    print("\n📊 RESULTADOS DEL ANÁLISIS:")
    for mood, t_list in categories.items():
        print(f"- {mood}: {len(t_list)} canciones")
    
    if all(len(v) == 0 for v in categories.values()):
        print("\n⚠️ No se encontraron canciones que encajen en estas categorías con los parámetros actuales.")
        return

    original_name = "Liked Songs" if mode == "liked_songs" else sp.playlist(pl_id, fields="name")['name']
    
    print(f"\n¿Quieres crear las playlists correspondientes para '{original_name}'?")
    confirm = input("Escribe 's' para confirmar o cualquier otra tecla para cancelar: ").strip().lower()
    
    if confirm == 's':
        create_mood_playlists(categories, original_name)
    else:
        print("🛑 Operación cancelada por el usuario.")

if __name__ == "__main__":
    main()
