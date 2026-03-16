import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

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

def get_mood_filters():
    return {
        "1": ("Fiesta (Party)", {"min_danceability": 0.7, "min_energy": 0.7}),
        "2": ("Chill / Relajante", {"max_energy": 0.4, "max_valence": 0.5}),
        "3": ("Energía Positiva", {"min_valence": 0.7, "min_energy": 0.6}),
        "4": ("Melancólico", {"max_valence": 0.3, "max_energy": 0.5}),
        "5": ("Concentración (Focus)", {"max_speechiness": 0.1, "max_energy": 0.5})
    }

def filter_tracks(tracks_with_features, criteria):
    filtered_ids = []
    for track_id, feat in tracks_with_features.items():
        if not feat: continue
        match = True
        for key, value in criteria.items():
            if key.startswith("min_"):
                feat_key = key.replace("min_", "")
                if feat[feat_key] < value: match = False
            elif key.startswith("max_"):
                feat_key = key.replace("max_", "")
                if feat[feat_key] > value: match = False
        if match:
            filtered_ids.append(track_id)
    return filtered_ids

def main():
    try:
        user_id = sp.me()['id']
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    print("\n=== MOOD MIXER (Mezclador por Estado de Ánimo) ===")
    mode, pl_id = select_playlist(sp, "SELECCIONA UNA LISTA PARA FILTRAR", include_liked=True)
    if not mode: return

    tracks = get_all_tracks(sp, mode, pl_id)
    if not tracks: return

    # Obtener Audio Features en bloques de 100
    ids = [t['track']['id'] for t in tracks if t['track'] and t['track']['id']]
    print(f"🔍 Analizando características de {len(ids)} canciones...")
    
    features_map = {}
    for i in range(0, len(ids), 100):
        batch = ids[i:i+100]
        feats = sp.audio_features(batch)
        for j, f in enumerate(feats):
            if f:
                features_map[batch[j]] = f
        print(f"   ∟ Procesadas {min(i+100, len(ids))}...")

    moods = get_mood_filters()
    while True:
        print("\n¿Qué estado de ánimo buscas?")
        for k, v in moods.items():
            print(f"{k}: {v[0]}")
        print("q: Salir")
        
        choice = input("\nElige una opción: ").strip().lower()
        if choice == 'q': break
        
        if choice in moods:
            name, criteria = moods[choice]
            filtered = filter_tracks(features_map, criteria)
            
            if not filtered:
                print(f"⚠️ No se encontraron canciones que coincidan con '{name}'.")
                continue
            
            pl_name = f"{name} Mix"
            print(f"✅ ¡Encontradas {len(filtered)} canciones! Creando '{pl_name}'...")
            
            new_pl = sp.user_playlist_create(user_id, pl_name, public=False)
            for i in range(0, len(filtered), 100):
                sp.playlist_add_items(new_pl['id'], filtered[i:i+100])
            print("🎉 Playlist creada con éxito.")
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    main()
