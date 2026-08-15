import os
import sys
import json
import csv
from utils.auth import get_spotify_client, SpotifyAuthError
from utils.helpers import select_playlist, get_all_tracks, format_duration, get_export_dir

try:
    sp = get_spotify_client()
except SpotifyAuthError as e:
    print(f"❌ Auth error: {e}")
    sys.exit(1)

import argparse

def flatten_track(item):
    """Extrae y aplanan los datos de una canción para su exportación."""
    track = item.get('track', {})
    if not track:
        return None
    
    return {
        "Name": track.get('name', 'Unknown'),
        "Artists": ", ".join([a['name'] for a in track.get('artists', [])]),
        "Album": track.get('album', {}).get('name', 'Unknown'),
        "Release Date": track.get('album', {}).get('release_date', ''),
        "Duration": format_duration(track.get('duration_ms', 0)),
        "Popularity": track.get('popularity', 0),
        "ISRC": track.get('external_ids', {}).get('isrc', ''),
        "URI": track.get('uri', '')
    }

def export_to_csv(tracks, filename, is_migration=False):
    if not tracks:
        print("⚠️ No hay canciones para exportar.")
        return

    if is_migration:
        # Formato compatible con Soundiiz/TuneMyMusic
        keys = ["title", "artist", "album", "isrc"]
    else:
        keys = ["Name", "Artists", "Album", "Release Date", "Duration", "Popularity", "ISRC", "URI"]
        
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            for t in tracks:
                flat_track = flatten_track(t)
                if not flat_track: continue
                
                if is_migration:
                    dict_writer.writerow({
                        "title": flat_track['Name'],
                        "artist": flat_track['Artists'],
                        "album": flat_track['Album'],
                        "isrc": flat_track['ISRC']
                    })
                else:
                    dict_writer.writerow(flat_track)
        print(f"✅ Exportado a CSV: {filename}")
    except Exception as e:
        print(f"❌ Error al exportar CSV: {e}")

def export_to_json(tracks, filename):
    if not tracks:
        print("⚠️ No hay canciones para exportar.")
        return

    data = []
    for t in tracks:
        flat = flatten_track(t)
        if flat:
            data.append(flat)
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ Exportado a JSON: {filename}")
    except Exception as e:
        print(f"❌ Error al exportar JSON: {e}")

def main():
    parser = argparse.ArgumentParser(description="Exporta metadatos de Spotify a CSV o JSON.")
    parser.add_argument("--playlist", help="ID de la playlist (o 'liked' para canciones favoritas)")
    parser.add_argument("--format", choices=["csv", "json", "all", "migration"], help="Formato de exportación")
    parser.add_argument("--output", help="Nombre del archivo de salida (opcional)")
    
    args = parser.parse_args()

    # Si se pasan argumentos, usamos el modo CLI
    if args.playlist and args.format:
        mode = "liked_songs" if args.playlist.lower() == "liked" else "playlist"
        pl_id = None if mode == "liked_songs" else args.playlist
        
        tracks = get_all_tracks(sp, mode, pl_id)
        if not tracks: return

        if args.output:
            base_name = args.output.rsplit('.', 1)[0]
        else:
            if mode == "liked_songs":
                base_name = "Liked_Songs"
            else:
                pl_info = sp.playlist(pl_id, fields="name")
                base_name = pl_info['name'].replace(" ", "_").replace("/", "-")

        export_dir = get_export_dir()
        if args.format in ['csv', 'all']:
            export_to_csv(tracks, os.path.join(export_dir, f"{base_name}.csv"))
        if args.format in ['migration', 'all']:
            export_to_csv(tracks, os.path.join(export_dir, f"{base_name}_migration.csv"), is_migration=True)
        if args.format in ['json', 'all']:
            export_to_json(tracks, os.path.join(export_dir, f"{base_name}.json"))
        return

    # Si no hay argumentos, iniciamos el modo interactivo
    print("\n=== EXPORTAR METADATOS (CSV/JSON) ===")
    mode, pl_id = select_playlist(sp, "SELECCIONA UNA LISTA PARA EXPORTAR", include_liked=True)
    if not mode: return

    tracks = get_all_tracks(sp, mode, pl_id)
    if not tracks:
        print("⚠️ No hay canciones para exportar.")
        return

    print("\n¿En qué formato quieres exportar?")
    print("1: CSV Estándar (Completo)")
    print("2: CSV Migración (Soundiiz/TuneMyMusic/Apple/YT)")
    print("3: JSON (Estándar de datos)")
    print("4: Todos los anteriores")
    print("q: Cancelar")

    choice = input("\nElige una opción: ").strip().lower()
    if choice == 'q': return

    if mode == "liked_songs":
        base_name = "Liked_Songs"
    else:
        pl_info = sp.playlist(pl_id, fields="name")
        base_name = pl_info['name'].replace(" ", "_").replace("/", "-")

    export_dir = get_export_dir()
    if choice in ['1', '4']:
        export_to_csv(tracks, os.path.join(export_dir, f"{base_name}_metadata.csv"))
    if choice in ['2', '4']:
        export_to_csv(tracks, os.path.join(export_dir, f"{base_name}_migration.csv"), is_migration=True)
    if choice in ['3', '4']:
        export_to_json(tracks, os.path.join(export_dir, f"{base_name}_metadata.json"))

    if choice not in ['1', '2', '3', '4']:
        print("❌ Opción no válida.")

if __name__ == "__main__":
    main()

