import sys
import os
import locale

def get_export_dir():
    """
    Retorna la ruta absoluta de la carpeta 'exports'.
    Si se ejecuta como EXE, usa la ruta del ejecutable.
    Si se ejecuta como script, usa la raíz del proyecto.
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller: Directorio del ejecutable (.exe)
        base_path = os.path.dirname(sys.executable)
    else:
        # Script: Raíz del proyecto (subiendo un nivel desde utils/)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    export_path = os.path.join(base_path, "exports")
    if not os.path.exists(export_path):
        try:
            os.makedirs(export_path, exist_ok=True)
        except:
            # Fallback a directorio actual si no hay permisos
            return os.getcwd()
            
    return export_path

def get_sys_lang():
    try:
        lang = locale.getlocale()[0]
        if lang and lang.lower().startswith('es'):
            return 'es'
    except:
        pass
    return 'en'

LANG = get_sys_lang()

HELP_TEXTS = {
    'es': {
        'loading': "🔍 Cargando tus playlists...",
        'liked_songs': "0: ❤️ Tus canciones favoritas (Liked Songs)",
        'tracks_count': "canciones",
        'selection_prompt': "\nSelección (número, nombre para buscar, o 'q' para cancelar): ",
        'out_of_range': "❌ Número fuera de rango.",
        'not_found': "❌ No se encontró ninguna playlist con",
        'selected': "✅ Seleccionada:",
        'matches_found': "🔍 Se encontraron {} coincidencias:",
        'write_exact': "\n💡 Escribe el número exacto ahora.",
        'getting_liked': "Obteniendo tus canciones favoritas ❤️...",
        'getting_playlist': "Obteniendo canciones de la playlist...",
        'total_obtained': "✅ Total de canciones obtenidas:"
    },
    'en': {
        'loading': "🔍 Loading your playlists...",
        'liked_songs': "0: ❤️ Your Liked Songs",
        'tracks_count': "tracks",
        'selection_prompt': "\nSelection (number, name to search, or 'q' to cancel): ",
        'out_of_range': "❌ Number out of range.",
        'not_found': "❌ No playlist found with",
        'selected': "✅ Selected:",
        'matches_found': "🔍 Found {} matches:",
        'write_exact': "\n💡 Type the exact number now.",
        'getting_liked': "Getting your Liked Songs ❤️...",
        'getting_playlist': "Getting playlist tracks...",
        'total_obtained': "✅ Total tracks obtained:"
    }
}

HT = HELP_TEXTS[LANG]

def get_user_playlists(sp):
    """Obtiene todas las playlists del usuario actual."""
    print(HT['loading'])
    playlists = []
    try:
        results = sp.current_user_playlists()
        while results:
            playlists.extend(results.get('items', []))
            results = sp.next(results) if results.get('next') else None
    except Exception as e:
        print(f"⚠️ Error al obtener playlists: {e}")
    return playlists

def select_playlist(sp, prompt="Elige una playlist:", include_liked=False):
    """Muestra una lista de playlists y permite al usuario seleccionar una."""
    playlists = get_user_playlists(sp)
    
    print(f"\n=== {prompt} ===")
    if include_liked:
        print(HT['liked_songs'])
        
    for i, pl in enumerate(playlists, start=1):
        name = pl.get('name', 'Unknown Playlist')
        tracks_info = pl.get('tracks', {})
        total_tracks = tracks_info.get('total', 0) if isinstance(tracks_info, dict) else 0
        print(f"{i}: {name} ({total_tracks} {HT['tracks_count']})")
    
    while True:
        raw_choice = input(HT['selection_prompt']).strip()
        if not raw_choice: continue
        choice = raw_choice.lower()

        if choice == 'q':
            return None, None
        
        if choice.isdigit():
            idx = int(choice)
            if idx == 0 and include_liked:
                return "liked_songs", None
            if 1 <= idx <= len(playlists):
                pl = playlists[idx-1]
                return "playlist", pl.get('id')
            print(HT['out_of_range'])
        else:
            # Búsqueda por nombre (manejando nombres nulos)
            matches = [pl for pl in playlists if choice.lower() in (pl.get('name') or "").lower()]
            if len(matches) == 0:
                print(f"{HT['not_found']} '{choice}'.")
            elif len(matches) == 1:
                pl = matches[0]
                name = pl.get('name', 'Unknown Playlist')
                print(f"{HT['selected']} {name}")
                return "playlist", pl.get('id')
            else:
                print(f"\n{HT['matches_found'].format(len(matches))}")
                for i, pl in enumerate(matches, start=1):
                    original_idx = playlists.index(pl) + 1
                    name = pl.get('name', 'Unknown Playlist')
                    tracks_info = pl.get('tracks', {})
                    total_tracks = tracks_info.get('total', 0) if isinstance(tracks_info, dict) else 0
                    print(f"{original_idx}: {name} ({total_tracks} {HT['tracks_count']})")
                print(HT['write_exact'])

def get_all_tracks(sp, mode, playlist_id=None, market=None):
    """Obtiene todas las canciones de una playlist o de 'Liked Songs' con reporte de progreso."""
    tracks = []
    try:
        if mode == "liked_songs":
            desc = HT['getting_liked']
            print(desc)
            results = sp.current_user_saved_tracks(limit=50, market=market)
            total = results.get('total', 0)
        else:
            desc = HT['getting_playlist']
            print(desc)
            results = sp.playlist_tracks(playlist_id, market=market)
            total = results.get('total', 0)
        
        fetched = 0
        while results:
            items = results.get('items', [])
            tracks.extend(items)
            fetched += len(items)
            
            # Reportar progreso
            if total > 0:
                percent = int((fetched / total) * 100)
                print(f"PROG:{percent}")
                sys.stdout.flush()

            results = sp.next(results) if results.get('next') else None
    except Exception as e:
        print(f"⚠️ Error al obtener canciones: {e}")
    
    # Filtrar tracks válidos
    tracks = [t for t in tracks if t and isinstance(t, dict) and t.get('track') and t['track'].get('id')]
    print(f"\n{HT['total_obtained']} {len(tracks)}")
    print("PROG:100") # Aseguramos bandera al terminar
    return tracks

def format_duration(ms):
    """Formatea milisegundos a un formato legible (HH:MM:SS o MM:SS)."""
    if ms is None or not isinstance(ms, (int, float)):
        return "0s"
    
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
