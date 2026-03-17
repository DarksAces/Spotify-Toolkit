import os
import sys
import json
import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --- CONFIGURACIÓN Y AUTENTICACIÓN ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

try:
    from utils.auth import get_spotify_client
    from utils.helpers import select_playlist, get_all_tracks, format_duration
    sp = get_spotify_client()
except ImportError:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope='user-library-read playlist-read-private'
    ))

def export_to_csv(tracks, filename):
    keys = ["Name", "Artists", "Album", "Release Date", "Duration", "Popularity", "URI"]
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            for t in tracks:
                track = t['track']
                dict_writer.writerow({
                    "Name": track['name'],
                    "Artists": ", ".join([a['name'] for a in track['artists']]),
                    "Album": track['album']['name'],
                    "Release Date": track['album']['release_date'],
                    "Duration": format_duration(track['duration_ms']),
                    "Popularity": track['popularity'],
                    "URI": track['uri']
                })
        print(f"✅ Exportado a CSV: {filename}")
    except Exception as e:
        print(f"❌ Error al exportar CSV: {e}")

def export_to_json(tracks, filename):
    data = []
    for t in tracks:
        track = t['track']
        data.append({
            "name": track['name'],
            "artists": [a['name'] for a in track['artists']],
            "album": track['album']['name'],
            "release_date": track['album']['release_date'],
            "duration_ms": track['duration_ms'],
            "duration_readable": format_duration(track['duration_ms']),
            "popularity": track['popularity'],
            "uri": track['uri']
        })
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ Exportado a JSON: {filename}")
    except Exception as e:
        print(f"❌ Error al exportar JSON: {e}")

def main():
    print("\n=== EXPORTAR METADATOS (CSV/JSON) ===")
    mode, pl_id = select_playlist(sp, "SELECCIONA UNA LISTA PARA EXPORTAR", include_liked=True)
    if not mode: return

    tracks = get_all_tracks(sp, mode, pl_id)
    if not tracks:
        print("⚠️ No hay canciones para exportar.")
        return

    print("\n¿En qué formato quieres exportar?")
    print("1: CSV (Compatible con Excel/Sheets)")
    print("2: JSON (Estándar de datos)")
    print("3: Ambos")
    print("q: Cancelar")

    choice = input("\nElige una opción: ").strip().lower()
    if choice == 'q': return

    # Buscar nombre de la playlist para el nombre del archivo
    if mode == "liked_songs":
        base_name = "Liked_Songs"
    else:
        pl_info = sp.playlist(pl_id, fields="name")
        base_name = pl_info['name'].replace(" ", "_").replace("/", "-")

    if choice in ['1', '3']:
        export_to_csv(tracks, f"{base_name}_metadata.csv")
    if choice in ['2', '3']:
        export_to_json(tracks, f"{base_name}_metadata.json")

    if choice not in ['1', '2', '3']:
        print("❌ Opción no válida.")

if __name__ == "__main__":
    main()
