import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm

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
        scope='playlist-modify-public playlist-modify-private user-library-read user-top-read user-read-recently-played'
    ))

def buscar_y_añadir():
    print("\n--- AÑADIR CANCIONES ---")
    mode, pl_id = select_playlist(sp, "Elige una playlist para añadir canciones")
    if not mode: return

    while True:
        query = input("\n🔍 Busca una canción (o 'fin' para terminar): ").strip()
        if query.lower() == 'fin': break
        if not query: continue

        results = sp.search(q=query, limit=5, type='track')
        tracks = results['tracks']['items']

        if not tracks:
            print("❌ No se encontraron canciones.")
            continue

        print("\nResultados:")
        for i, track in enumerate(tracks):
            artists = ", ".join([a['name'] for a in track['artists']])
            print(f"{i+1}: {track['name']} - {artists}")
        
        choice = input("\nElige el número para añadir (o 'c' para cancelar): ").strip().lower()
        if choice == 'c': continue
        
        if choice.isdigit() and 1 <= int(choice) <= len(tracks):
            track_to_add = tracks[int(choice)-1]
            try:
                sp.playlist_add_items(pl_id, [track_to_add['uri']])
                print(f"✅ Añadida: {track_to_add['name']}")
            except Exception as e:
                print(f"❌ Error al añadir: {e}")
        else:
            print("❌ Opción no válida.")

def obtener_recomendaciones():
    print("\n--- RECOMENDACIONES PERSONALIZADAS ---")
    print("¿En qué basamos las recomendaciones?")
    print("1: Mis Top Canciones (recientes)")
    print("2: Mis Top Artistas (recientes)")
    print("3: Lo último que he escuchado")
    print("q: Cancelar")

    choice = input("\nElige una opción: ").strip().lower()
    if choice == 'q': return

    seed_tracks = []
    seed_artists = []

    try:
        if choice == '1':
            print("⏳ Obteniendo tus canciones favoritas...")
            top_tracks = sp.current_user_top_tracks(limit=5, time_range='short_term')['items']
            seed_tracks = [t['id'] for t in top_tracks]
        elif choice == '2':
            print("⏳ Obteniendo tus artistas favoritos...")
            top_artists = sp.current_user_top_artists(limit=5, time_range='short_term')['items']
            seed_artists = [a['id'] for a in top_artists]
        elif choice == '3':
            print("⏳ Obteniendo tus últimas canciones escuchadas...")
            recent = sp.current_user_recently_played(limit=5)['items']
            seed_tracks = [t['track']['id'] for t in recent]
        else:
            print("❌ Opción no válida.")
            return

        if not seed_tracks and not seed_artists:
            print("❌ No hay suficientes datos para generar recomendaciones.")
            return

        print("🚀 Generando recomendaciones...")
        recommendations = sp.recommendations(seed_tracks=seed_tracks, seed_artists=seed_artists, limit=20)
        rec_tracks = recommendations['tracks']

        if not rec_tracks:
            print("⚠️ No se encontraron recomendaciones.")
            return

        print(f"\n✨ Hemos encontrado {len(rec_tracks)} canciones para ti:")
        for i, track in enumerate(rec_tracks):
            artists = ", ".join([a['name'] for a in track['artists']])
            print(f" - {track['name']} ({artists})")

        confirm = input("\n¿Quieres guardar estas recomendaciones en una nueva playlist? (s/n): ").strip().lower()
        if confirm == 's':
            name = input("Nombre de la playlist: ").strip()
            if not name: name = "Descubrimiento Personalizado"
            
            user_id = sp.me()['id']
            new_pl = sp.user_playlist_create(user_id, name, public=False)
            uris = [t['uri'] for t in rec_tracks]
            sp.playlist_add_items(new_pl['id'], uris)
            print(f"✅ ¡Hecho! Playlist '{name}' creada con éxito.")

    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    while True:
        print("\n=== DISCOVERY ENGINE (Descubrimiento y Búsqueda) ===")
        print("1: Buscar y añadir canciones a una playlist")
        print("2: Obtener recomendaciones basadas en mis gustos")
        print("q: Salir")

        choice = input("\nElige una opción: ").strip().lower()

        if choice == '1':
            buscar_y_añadir()
        elif choice == '2':
            obtener_recomendaciones()
        elif choice == 'q':
            break
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    main()
