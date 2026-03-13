import sys
import os

def get_user_playlists(sp):
    """Obtiene todas las playlists del usuario actual."""
    print("🔍 Cargando tus playlists...")
    playlists = []
    results = sp.current_user_playlists()
    playlists.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])
    return playlists

def select_playlist(sp, prompt="Elige una playlist:", include_liked=False):
    """Muestra una lista de playlists y permite al usuario seleccionar una."""
    playlists = get_user_playlists(sp)
    
    print(f"\n=== {prompt} ===")
    if include_liked:
        print("0: ❤️ Tus canciones favoritas (Liked Songs)")
        
    for i, pl in enumerate(playlists, start=1):
        print(f"{i}: {pl['name']} ({pl['tracks']['total']} canciones)")
    
    while True:
        choice = input(f"\nSelección (o 'q' para cancelar): ").strip()
        if choice.lower() == 'q':
            return None, None
        
        if choice.isdigit():
            idx = int(choice)
            if idx == 0 and include_liked:
                return "liked_songs", None
            if 1 <= idx <= len(playlists):
                pl = playlists[idx-1]
                return "playlist", pl['id']
        
        print("❌ Selección no válida. Inténtalo de nuevo.")

def get_all_tracks(sp, mode, playlist_id=None):
    """Obtiene todas las canciones de una playlist o de 'Liked Songs'."""
    tracks = []
    if mode == "liked_songs":
        print("Obteniendo tus canciones favoritas ❤️...")
        results = sp.current_user_saved_tracks(limit=50)
        tracks.extend(results['items'])
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
    else:
        print(f"Obteniendo canciones de la playlist...")
        results = sp.playlist_tracks(playlist_id)
        tracks.extend(results['items'])
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
    
    # Filtrar tracks válidos
    tracks = [t for t in tracks if t and t.get('track')]
    print(f"✅ Total de canciones obtenidas: {len(tracks)}")
    return tracks

def format_duration(ms):
    """Formatea milisegundos a un formato legible (HH:MM:SS o MM:SS)."""
    seconds = int((ms / 1000) % 60)
    minutes = int((ms / (1000 * 60)) % 60)
    hours = int((ms / (1000 * 60 * 60)) % 24)
    days = int(ms / (1000 * 60 * 60 * 24))

    parts = []
    if days > 0: parts.append(f"{days}d")
    if hours > 0: parts.append(f"{hours}h")
    if minutes > 0: parts.append(f"{minutes}m")
    if seconds > 0 or not parts: parts.append(f"{seconds}s")
    
    return " ".join(parts)
