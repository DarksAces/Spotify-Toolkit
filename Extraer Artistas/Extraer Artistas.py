import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import Counter
import time # Es crucial para manejar límites de tasa de la API

# --- Configuración (Actionable: Reemplaza tus credenciales) ---
CLIENT_ID = ''
CLIENT_SECRET = ''

# Autenticación
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

# --- Funciones de Utilidad ---

def obtener_generos_artista(artist_id):
    """
    Obtiene la lista de géneros para un artista dado su ID de Spotify.
    
    Returns:
        list: Lista de strings con los géneros.
    """
    try:
        # Llamada a la API para obtener la metadata del artista
        artist_info = sp.artist(artist_id)
        # Los géneros se devuelven en minúsculas y sin mayúsculas
        return artist_info.get('genres', []) 
    except Exception as e:
        print(f"  [ADVERTENCIA] Error al obtener info del artista {artist_id}. Saltando. ({e})")
        time.sleep(1) 
        return []

def obtener_datos_playlist(playlist_url):
    """
    Extrae todos los artistas de una playlist, registrando todas las apariciones
    y mapeando artistas únicos a sus IDs.
    
    Returns:
        list: Lista de todos los nombres de artistas (con repeticiones).
        dict: Mapeo de Artista_Nombre -> Artista_ID (solo artistas únicos).
    """
    print(f"\n[INFO] Procesando playlist: {playlist_url} ⏳")
    
    if 'playlist/' in playlist_url:
        playlist_id = playlist_url.split('playlist/')[-1].split('?')[0]
    else:
        playlist_id = playlist_url
    
    todos_los_artistas_nombres = []
    artista_a_id = {}
    
    try:
        resultados = sp.playlist_tracks(playlist_id)
    except Exception as e:
        print(f"[ERROR] No se pudo acceder a la playlist {playlist_id}. ({e})")
        return [], {}
        
    tracks = resultados['items']
    print(f"   ∟ Obtenidas {len(tracks)} canciones...")
    while resultados['next']:
        resultados = sp.next(resultados)
        tracks.extend(resultados['items'])
        print(f"   ∟ Obtenidas {len(tracks)} canciones...")
    
    # Procesar todos los tracks
    for item in tracks:
        if item and item.get('track') and item['track'].get('artists'):
            for artist in item['track']['artists']:
                artist_name = artist['name']
                # 1. Almacenamos CADA aparición para el conteo posterior
                todos_los_artistas_nombres.append(artist_name)
                # 2. Almacenamos el ID SÓLO si es un artista nuevo para mapeo
                if artist_name not in artista_a_id:
                    artista_a_id[artist_name] = artist['id']
    
    print(f"[OK] {len(tracks)} tracks procesados. Artistas únicos: {len(artista_a_id)}")
    
    return todos_los_artistas_nombres, artista_a_id

# --- Punto de Entrada del Pipeline ---
if __name__ == "__main__":
    
    # 🎯 INPUT: Define las URLs de las playlists a analizar
    playlist_urls = [
        "",  # Playlist 1: (Ejemplo)
        ""   # Playlist 2: (Ejemplo)
    ]
    
    # Contenedores de datos
    todos_los_artistas_agregados = []
    mapeo_artista_a_id = {}
    
    # FASE 1: EXTRACCIÓN Y CONSOLIDACIÓN DE ARTISTAS
    print("--- 🏁 FASE 1: Extracción y Consolidación de Artistas ---")
    for url in playlist_urls:
        nombres, mapeo_id = obtener_datos_playlist(url)
        todos_los_artistas_agregados.extend(nombres)
        mapeo_artista_a_id.update(mapeo_id) 
        
    # Conteo de artistas (para el peso ponderado)
    conteo_total_artistas = Counter(todos_los_artistas_agregados)
    
    
    # FASE 2: MAPEO DE GÉNEROS Y GENERACIÓN DE ARCHIVOS
    print("\n--- 🛠️ FASE 2: Mapeo de Géneros y Generación de Archivos ---")
    
    # Contenedores para el reporte
    mapeo_generos_por_artista = {} # Almacena Artista -> Géneros
    conteo_generos = Counter()      # Almacena Género -> Peso Ponderado
    
    total_artistas_unicos = len(mapeo_artista_a_id)
    artistas_procesados = 0

    with open('mapeo_artista_genero.txt', 'w', encoding='utf-8') as f_mapeo:
        f_mapeo.write("Artista,Géneros\n")
        
        for artista, artist_id in mapeo_artista_a_id.items():
            if not artist_id: 
                continue
                
            # 2.1 Obtener los géneros del artista
            generos = obtener_generos_artista(artist_id)
            peso_del_artista = conteo_total_artistas[artista]
            
            # 2.2 Generar el archivo de mapeo (Artista, Géneros)
            generos_csv = ' | '.join([g.title() for g in generos]) # Usamos '|' como separador en el archivo
            f_mapeo.write(f"{artista},{generos_csv}\n")
            mapeo_generos_por_artista[artista] = generos # Guardamos para referencia
            
            # 2.3 Ponderación y Conteo (para el reporte final)
            for genero in generos:
                conteo_generos[genero.title()] += peso_del_artista
            
            artistas_procesados += 1
            if artistas_procesados % 10 == 0 or artistas_procesados == total_artistas_unicos:
                print(f"  Progreso de mapeo: {artistas_procesados}/{total_artistas_unicos} artistas procesados...")

    print("\n✓ Archivo de mapeo guardado en 'mapeo_artista_genero.txt'")

    # FASE 3: GENERACIÓN DEL REPORTE FINAL DE CONTEO
    print("\n--- 📊 FASE 3: Generación de Reporte de Frecuencia de Géneros ---")
    
    if conteo_generos:
        conteo_ordenado = conteo_generos.most_common()
        
        # Presentación en consola
        print("\n--- Top Géneros (Consolidado) ---")
        for genero, peso in conteo_ordenado[:10]: # Muestra solo los 10 primeros en consola
            print(f"**{genero}**: {peso} apariciones ponderadas")
            
        # Generación del archivo CSV de conteo
        with open('conteo_generos_consolidado.txt', 'w', encoding='utf-8') as f_conteo:
            f_conteo.write("Genero,Peso_en_Playlist\n")
            for genero, peso in conteo_ordenado:
                 f_conteo.write(f"{genero},{peso}\n")
                 
        print("\n✓ Reporte de frecuencias CONSOLIDADO guardado en 'conteo_generos_consolidado.txt'")
        
    else:
        print("El proceso finalizó sin datos de género válidos.")