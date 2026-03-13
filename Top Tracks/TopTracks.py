import os
import random
import spotipy
import sys
from spotipy.oauth2 import SpotifyOAuth
from difflib import SequenceMatcher

# --- CONFIGURACIÓN Y AUTENTICACIÓN ---
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope='user-library-read playlist-read-private playlist-modify-public playlist-modify-private'
))
usuario_id = sp.current_user()['id']

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def buscar_artista_inteligente(nombre_buscado):
    print(f"🔍 Buscando '{nombre_buscado}'...")
    resultados = sp.search(q=f'artist:"{nombre_buscado}"', type="artist", limit=10)
    items = resultados['artists']['items']
    
    if not items:
        # Intento de búsqueda más abierta si falla la exacta
        resultados = sp.search(q=nombre_buscado, type="artist", limit=10)
        items = resultados['artists']['items']
    
    if not items: return None

    # Primero buscamos coincidencia exacta (sin contar mayúsculas)
    for artista in items:
        if artista['name'].lower() == nombre_buscado.lower():
            return artista

    # Si no hay exacta, buscamos la más similar
    mejor_coincidencia = max(items, key=lambda a: similar(nombre_buscado, a['name']))
    ratio = similar(nombre_buscado, mejor_coincidencia['name'])
    
    if ratio > 0.6: # Si se parece más de un 60%
        print(f"❓ No encontré '{nombre_buscado}', ¿te refieres a '{mejor_coincidencia['name']}'?")
        confirmar = input("Pulsa 's' para confirmar o cualquier otra tecla para saltar: ").strip().lower()
        if confirmar == 's':
            return mejor_coincidencia
            
    return None

def main():
    todas_canciones_uris = []
    
    while True:
        print("\n=== GENERADOR DE PLAYLIST POR ARTISTA ===")
        entrada = input("Escribe el nombre de un artista (o 'fin' para terminar): ").strip()
        if entrada.lower() == 'fin': break
        
        artista = buscar_artista_inteligente(entrada)
        if not artista:
            print("❌ No se encontró el artista.")
            continue

        print(f"✅ Artista encontrado: {artista['name']}")
        
        # Obtener Top Tracks
        try:
            top = sp.artist_top_tracks(artista['id'])['tracks']
            uris = [t['uri'] for t in top]
            todas_canciones_uris.extend(uris)
            print(f"   ∟ Añadidas {len(uris)} canciones de {artista['name']}.")
        except Exception as e:
            print(f"   ❌ Error obteniendo canciones: {e}")

    if not todas_canciones_uris:
        print("\nNo se añadieron canciones. Saliendo...")
        return

    # Selección de Playlist
    print(f"\nSe han acumulado {len(todas_canciones_uris)} canciones.")
    nombre_pl = input("Nombre para la nueva playlist (o presiona Enter para 'Mix Temporal'): ").strip()
    if not nombre_pl: nombre_pl = "Mix Temporal Artistas"
    
    nueva_pl = sp.user_playlist_create(usuario_id, nombre_pl)
    for i in range(0, len(todas_canciones_uris), 100):
        sp.playlist_add_items(nueva_pl['id'], todas_canciones_uris[i:i+100])
    
    print(f"\n🎉 ¡Hecho! Playlist '{nombre_pl}' creada con éxito.")

if __name__ == "__main__":
    main()