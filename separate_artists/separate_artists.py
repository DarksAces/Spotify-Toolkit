import time
import os
import sys
from utils.auth import get_spotify_client, SpotifyAuthError
from utils.helpers import select_playlist, get_all_tracks

try:
    sp = get_spotify_client()
except SpotifyAuthError as e:
    print(f"❌ Auth error: {e}")
    sys.exit(1)

def classify_tracks_by_artist(tracks):
    artist_dict = {}
    for item in tracks:
        track = item['track']
        if track and track['artists']:
            artist_name = track['artists'][0]['name']
            artist_dict.setdefault(artist_name, []).append(track['id'])
    return artist_dict

def classify_tracks_by_similar_artists(tracks):
    similar_artist_dict = {}
    total = len(tracks)
    print(f"\nAnalizando artistas similares para {total} canciones...")
    
    # Cache para no repetir búsquedas de artistas relacionados
    related_cache = {}

    with tqdm(total=total, desc="Analizando similares", unit="track") as pbar:
        for idx, item in enumerate(tracks, 1):
            track = item['track']
            if not track or not track['artists']: 
                pbar.update(1)
                continue
            
            artist = track['artists'][0]
            artist_id = artist['id']
            artist_name = artist['name']

            if artist_id not in related_cache:
                while True:
                    try:
                        related = sp.artist_related_artists(artist_id)['artists']
                        related_cache[artist_id] = [r['name'] for r in related]
                        break
                    except ReadTimeout:
                        time.sleep(2)
                    except SpotifyException as e:
                        if e.http_status == 429:
                            time.sleep(int(e.headers.get('Retry-After', 1)))
                        else: raise e

            for related_name in related_cache[artist_id]:
                similar_artist_dict.setdefault(related_name, []).append(track['id'])
            
            pbar.update(1)

    return similar_artist_dict

def main():
    try:
        user_id = sp.me()['id']
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    mode, pl_id = select_playlist(sp, "SELECCIONA UNA LISTA PARA SEPARAR", include_liked=True)
    if not mode: return

    tracks = get_all_tracks(sp, mode, pl_id)
    if not tracks: return

    print("\n¿Quieres agrupar por artista principal (A) o por artistas similares (S)?")
    choice = input("Selecciona (A/S): ").strip().lower()

    if choice == 'a':
        classified = classify_tracks_by_artist(tracks)
    elif choice == 's':
        classified = classify_tracks_by_similar_artists(tracks)
    else:
        print("❌ Opción inválida.")
        return

    # Mostrar resumen
    print(f"\nSe han detectado {len(classified)} grupos.")
    print("Creando playlists para grupos con más de 3 canciones...")

    for artist, ids in classified.items():
        if len(ids) >= 3:
            unique_ids = list(dict.fromkeys(ids))
            name = f"{artist} Mix"
            print(f"   ∟ Creando: {name} ({len(unique_ids)} tracks)")
            new_pl = sp.user_playlist_create(user_id, name, public=False)
            with tqdm(total=len(unique_ids), desc=f"Añadiendo tracks", unit="track", leave=False) as pbar:
                for i in range(0, len(unique_ids), 100):
                    batch = unique_ids[i:i+100]
                    sp.playlist_add_items(new_pl['id'], batch)
                    pbar.update(len(batch))

    print("\n✨ Proceso completado.")

if __name__ == "__main__":
    main()
