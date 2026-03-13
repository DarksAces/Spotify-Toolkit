import os
import random
import spotipy
import sys
from spotipy.oauth2 import SpotifyOAuth
from difflib import SequenceMatcher

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
        scope='user-library-read user-top-read playlist-read-private playlist-modify-public playlist-modify-private'
    ))

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def buscar_artista_inteligente(nombre_buscado):
    print(f"🔍 Buscando '{nombre_buscado}'...")
    resultados = sp.search(q=f'artist:"{nombre_buscado}"', type="artist", limit=10)
    items = resultados['artists']['items']
    
    if not items:
        resultados = sp.search(q=nombre_buscado, type="artist", limit=10)
        items = resultados['artists']['items']
    
    if not items: return None

    for artista in items:
        if artista['name'].lower() == nombre_buscado.lower():
            return artista

    mejor_coincidencia = max(items, key=lambda a: similar(nombre_buscado, a['name']))
    ratio = similar(nombre_buscado, mejor_coincidencia['name'])
    
    if ratio > 0.6:
        print(f"❓ No encontré '{nombre_buscado}', ¿te refieres a '{mejor_coincidencia['name']}'?")
        confirmar = input("Pulsa 's' para confirmar o cualquier otra tecla para saltar: ").strip().lower()
        if confirmar == 's':
            return mejor_coincidencia
            
    return None

def generar_playlist_usuario_top():
    print("\n--- GENERAR TUS TOP CANCIONES ---")
    print("1: Últimas 4 semanas (Short Term)")
    print("2: Últimos 6 meses (Medium Term)")
    print("3: Todo el tiempo (Long Term)")
    
    term_choice = input("Elige el periodo (1-3): ").strip()
    term_map = {"1": "short_term", "2": "medium_term", "3": "long_term"}
    term = term_map.get(term_choice, "medium_term")
    
    limit = input("¿Cuántas canciones? (máx 50, default 50): ").strip()
    limit = int(limit) if limit.isdigit() else 50
    
    print("🚀 Obteniendo tus canciones más escuchadas...")
    top_tracks = sp.current_user_top_tracks(limit=limit, time_range=term)['items']
    
    if not top_tracks:
        print("❌ No pude encontrar tus canciones más escuchadas.")
        return

    uris = [t['uri'] for t in top_tracks]
    
    nombre_pl = f"Mis Top {len(uris)} ({term.replace('_', ' ').title()})"
    user_id = sp.current_user()['id']
    nueva_pl = sp.user_playlist_create(user_id, nombre_pl, public=False)
    sp.playlist_add_items(nueva_pl['id'], uris)
    
    print(f"✅ ¡Hecho! Creada playlist '{nombre_pl}'")

def generar_playlist_artistas():
    print("\n--- GENERADOR DE PLAYLIST POR ARTISTAS ---")
    todas_uris = []
    user_id = sp.current_user()['id']
    
    while True:
        entrada = input("Escribe el nombre de un artista (o 'fin' para terminar): ").strip()
        if entrada.lower() == 'fin': break
        
        artista = buscar_artista_inteligente(entrada)
        if not artista:
            print("❌ No se encontró el artista.")
            continue

        print(f"✅ Artista encontrado: {artista['name']}")
        try:
            top = sp.artist_top_tracks(artista['id'])['tracks']
            uris = [t['uri'] for t in top]
            todas_uris.extend(uris)
            print(f"   ∟ Añadidas {len(uris)} canciones de {artista['name']}.")
        except Exception as e:
            print(f"   ❌ Error obteniendo canciones: {e}")

    if not todas_uris:
        print("No se añadieron canciones.")
        return

    nombre_pl = input("Nombre para la playlist: ").strip()
    if not nombre_pl: nombre_pl = "Mix de Artistas Seleccionados"
    
    nueva_pl = sp.user_playlist_create(user_id, nombre_pl)
    for i in range(0, len(todas_uris), 100):
        sp.playlist_add_items(nueva_pl['id'], todas_uris[i:i+100])
    
    print(f"✅ ¡Hecho! Playlist '{nombre_pl}' creada.")

def main():
    while True:
        print("\n=== ESTADÍSTICAS Y MEZCLA (Top Tracks) ===")
        print("1: Generar Playlist con MIS Top Canciones")
        print("2: Generar Mix de Artistas Específicos")
        print("q: Salir")
        
        choice = input("\nElige una opción: ").strip().lower()
        
        if choice == '1':
            generar_playlist_usuario_top()
        elif choice == '2':
            generar_playlist_artistas()
        elif choice == 'q':
            break
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    main()