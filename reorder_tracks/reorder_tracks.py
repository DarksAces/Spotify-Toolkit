import os
import sys
from utils.auth import get_spotify_client, SpotifyAuthError
from utils.helpers import select_playlist, get_all_tracks

try:
    sp = get_spotify_client()
except SpotifyAuthError as e:
    print(f"❌ Auth error: {e}")
    sys.exit(1)

def main():
    while True:
        print("\n=== REORDER TRACKS (Mover artista al final) ===")
        mode, pl_id = select_playlist(sp, "SELECCIONA UNA LISTA", include_liked=True)
        
        if not mode: break
        if mode == "liked_songs":
            print("⚠️ No se puede reordenar 'Favoritos' vía API.")
            print("Se recomienda crear una nueva playlist.")
            continue

        tracks = get_all_tracks(sp, mode, pl_id)
        if not tracks: continue

        artist_target = input("\n🎤 Artista que quieres mover al final: ").lower().strip()
        
        # Encontrar índices de canciones del artista
        matches = []
        for i, item in enumerate(tracks):
            if not item['track']: continue
            track_artists = [a['name'].lower().strip() for a in item['track']['artists']]
            if any(artist_target in a for a in track_artists):
                matches.append(i)

        if not matches:
            print(f"⚠️ No se encontraron canciones de '{artist_target}'.")
            continue

        print(f"✅ Se han encontrado {len(matches)} canciones.")

        print("📤 Moviendo canciones al final...")
        
        # Reordenar en orden inverso para no alterar los índices de las de arriba
        total_tracks = len(tracks)
        with tqdm(total=len(matches), desc="Reordenando tracks", unit="track") as pbar:
            for i, idx in enumerate(sorted(matches, reverse=True)):
                # Spotify playlist_reorder_items(playlist_id, range_start, insert_before)
                sp.playlist_reorder_items(pl_id, range_start=idx, insert_before=total_tracks)
                
                pbar.update(1)
                # Reportar progreso a la interfaz
                percent = int(((i + 1) / len(matches)) * 100)
                print(f"PROG:{percent}")
                sys.stdout.flush()
        
        print(f"\n✅ ¡Hecho! {len(matches)} canciones movidas al final.")

        otra = input("\n¿Quieres reordenar otra? (s/n): ").strip().lower()
        if otra != 's': break

if __name__ == "__main__":
    main()
