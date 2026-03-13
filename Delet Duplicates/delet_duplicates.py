import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyOauthError
from collections import defaultdict

# ------------------- AUTENTICACIÓN -------------------
def get_spotify_client():
    try:
        return spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope='user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'
        ))
    except SpotifyOauthError as e:
        print(f"\n❌ Error de autenticación: {e}")
        sys.exit()

sp = get_spotify_client()

def get_user_playlists():
    print("🔍 Cargando tus playlists...")
    results = sp.current_user_playlists()
    playlists = results['items']
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])
    return playlists

def process_duplicates():
    playlists = get_user_playlists()
    
    while True:
        print("\n=== SELECTOR DE PLAYLIST (Limpieza de Duplicados) ===")
        print("0: ❤️ Tus canciones favoritas (Liked Songs)")
        for idx, pl in enumerate(playlists, start=1):
            print(f"{idx}: {pl['name']} ({pl['tracks']['total']} canciones)")
        
        choice = input("\nElige el número de la lista o 'q' para salir: ").strip()
        if choice.lower() == 'q': break
        
        if not choice.isdigit(): continue
        
        idx = int(choice)
        tracks = []
        playlist_id = None
        playlist_name = ""

        if idx == 0:
            print("\n🔍 Obteniendo tus canciones favoritas...")
            playlist_name = "Tus canciones favoritas ❤️"
            results = sp.current_user_saved_tracks(limit=50)
            tracks.extend(results['items'])
            print(f"   ∟ Obtenidas {len(tracks)} canciones...")
            while results['next']:
                results = sp.next(results)
                tracks.extend(results['items'])
                print(f"   ∟ Obtenidas {len(tracks)} canciones...")
        elif 1 <= idx <= len(playlists):
            playlist = playlists[idx - 1]
            playlist_id = playlist['id']
            playlist_name = playlist['name']
            print(f"\n🔍 Obteniendo canciones de '{playlist_name}'...")
            offset = 0
            while True:
                results = sp.playlist_items(playlist_id, offset=offset, fields="items.track.id,items.track.name,items.track.artists(name),next")
                tracks.extend(results["items"])
                print(f"   ∟ Obtenidas {len(tracks)} canciones...")
                if results["next"] is None: break
                offset += len(results["items"])
        else:
            print("❌ Opción no válida.")
            continue

        # --- DETECTAR DUPLICADOS ---
        print(f"\nAnalizando {len(tracks)} canciones...")
        duplicados_grupos = defaultdict(list)
        for i, item in enumerate(tracks):
            track = item["track"]
            if not track: continue
            name = track["name"].strip().lower()
            artists = ", ".join([a["name"].strip().lower() for a in track["artists"]])
            clave = (name, artists)
            duplicados_grupos[clave].append({"track": track, "pos": i + 1})

        duplicados_grupos = {k: v for k, v in duplicados_grupos.items() if len(v) > 1}

        if not duplicados_grupos:
            print("\n✅ No se encontraron duplicados en esta lista.")
        else:
            print(f"\n⚠️ Se encontraron {len(duplicados_grupos)} grupos de duplicados.")
            borrar_todas = input("¿Quieres mantener solo una copia de cada una? (S/n): ").strip().lower()
            
            tracks_to_delete = []
            if borrar_todas == 's':
                for group in duplicados_grupos.values():
                    for item in group[1:]:
                        tracks_to_delete.append(item['track']['id'])
            
            if tracks_to_delete and playlist_id:
                for i in range(0, len(tracks_to_delete), 100):
                    sp.playlist_remove_all_occurrences_of_items(playlist_id, tracks_to_delete[i:i+100])
                print(f"\n✅ ¡Limpieza completada! Se eliminaron {len(tracks_to_delete)} duplicados.")
            elif not playlist_id:
                print("\n⚠️ No se pueden borrar canciones directamente de 'Favoritos' vía API.")
                print("Crea una nueva playlist limpia si quieres deshacerte de ellos.")

        otra = input("\n¿Quieres limpiar otra playlist? (s/n): ").strip().lower()
        if otra != 's': break

if __name__ == "__main__":
    process_duplicates()
    print("\n👋 ¡Hasta luego!")
