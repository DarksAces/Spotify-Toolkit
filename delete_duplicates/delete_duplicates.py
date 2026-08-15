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
        print("\n=== DELETE DUPLICATES (Limpieza de Playlist) ===")
        mode, pl_id = select_playlist(sp, "SELECCIONA UNA LISTA PARA LIMPIAR", include_liked=True)
        
        if not mode: break

        tracks = get_all_tracks(sp, mode, pl_id)
        if not tracks: continue

        # Detectar duplicados (por nombre y artista principal)
        print(f"\nAnalizando {len(tracks)} canciones...")
        vistos = {}
        to_remove = []

        for item in tracks:
            track = item['track']
            if not track or not track['id']: continue
            
            # Clave: (Nombre, Primer Artista) para detectar versiones similares
            key = (track['name'].lower().strip(), track['artists'][0]['name'].lower().strip())
            
            if key in vistos:
                to_remove.append(track['id'])
            else:
                vistos[key] = track['id']

        if not to_remove:
            print("✅ No se encontraron duplicados.")
        else:
            print(f"⚠️ Se han encontrado {len(to_remove)} duplicados.")
            confirm = input(f"¿Quieres eliminar {len(to_remove)} canciones duplicadas? (s/n): ").strip().lower()
            
            if confirm == 's':
                if mode == "liked_songs":
                    print("⚠️ La API de Spotify no permite borrar de 'Favoritos' por ID fácilmente.")
                    print("Se recomienda crear una nueva playlist sin duplicados.")
                    
                    crear = input("¿Quieres crear una nueva playlist 'Favoritos Limpios'? (s/n): ").strip().lower()
                    if crear == 's':
                        user_id = sp.me()['id']
                        new_pl = sp.user_playlist_create(user_id, "Favoritos Limpios", public=False)
                        all_ids = list(vistos.values())
                        total_to_add = len(all_ids)
                        with tqdm(total=total_to_add, desc="Creando playlist", unit="track") as pbar:
                            for i in range(0, total_to_add, 100):
                                batch = all_ids[i:i+100]
                                sp.playlist_add_items(new_pl['id'], batch)
                                pbar.update(len(batch))
                                # Progreso para la GUI
                                percent = int(((i + len(batch)) / total_to_add) * 100)
                                print(f"PROG:{min(percent, 100)}")
                                sys.stdout.flush()
                        print("✅ Playlist 'Favoritos Limpios' creada.")
                else:
                    # Borrar de playlist normal
                    total_to_remove = len(to_remove)
                    with tqdm(total=total_to_remove, desc="Eliminando duplicados", unit="track") as pbar:
                        for i in range(0, total_to_remove, 100):
                            batch = to_remove[i:i+100]
                            sp.playlist_remove_all_occurrences_of_items(pl_id, batch)
                            pbar.update(len(batch))
                            percent = int(((i + len(batch)) / total_to_remove) * 100)
                            print(f"PROG:{min(percent, 100)}")
                            sys.stdout.flush()
                    print(f"✅ Se han eliminado {len(to_remove)} duplicados de la playlist.")

        otra = input("\n¿Quieres limpiar otra playlist? (s/n): ").strip().lower()
        if otra != 's': break

if __name__ == "__main__":
    main()
