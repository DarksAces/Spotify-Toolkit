import os
import random
from utils.auth import get_spotify_client, SpotifyAuthError
from utils.helpers import select_playlist, get_all_tracks

try:
    sp = get_spotify_client()
except SpotifyAuthError as e:
    print(f"❌ Auth error: {e}")
    sys.exit(1)

def mezclar_flexible(tracks, max_intentos=5000):
    print(f"🎲 Iniciando Smart Shuffle para {len(tracks)} canciones...")
    if len(tracks) < 2: return tracks

    mejor_mezcla = list(tracks)
    min_colisiones = len(tracks)

    with tqdm(total=max_intentos, desc="Calculando mejor mezcla", unit="intento") as pbar:
        for intento in range(max_intentos):
            random.shuffle(tracks)
            colisiones = 0
            for i in range(1, len(tracks)):
                if tracks[i]['artist'] == tracks[i-1]['artist'] or tracks[i]['album'] == tracks[i-1]['album']:
                    colisiones += 1
            
            if colisiones == 0:
                pbar.update(max_intentos - intento)
                print(f"   ∟ Mezcla perfecta encontrada en intento {intento+1}!")
                return tracks
            
            if colisiones < min_colisiones:
                min_colisiones = colisiones
                mejor_mezcla = list(tracks)
            
            pbar.update(1)
            
    print(f"   ⚠️ No se encontró una mezcla perfecta. Usando la mejor (colisiones: {min_colisiones})")
    return mejor_mezcla

def main():
    while True:
        print("\n=== SMART SHUFFLE (Mezcla inteligente) ===")
        mode, pl_id = select_playlist(sp, "Elige la playlist para mezclar", include_liked=True)
        
        if not mode: break
        
        tracks_raw = get_all_tracks(sp, mode, pl_id)
        if not tracks_raw:
            print("❌ La lista está vacía.")
            continue

        canciones = []
        for item in tracks_raw:
            track = item['track']
            if track and track['uri'] and track['artists']:
                canciones.append({
                    "uri": track['uri'],
                    "artist": track['artists'][0]['name'],
                    "album": track['album']['name']
                })

        mezcladas = mezclar_flexible(canciones)
        
        print("📤 Actualizando playlist en Spotify...")
        uris = [t['uri'] for t in mezcladas]
        
        if mode == "liked_songs":
            print("⚠️ La API de Spotify no permite reordenar 'Liked Songs' directamente.")
            print("Creando una nueva playlist 'Smart Shuffle Liked'...")
            user_id = sp.me()['id']
            new_pl = sp.user_playlist_create(user_id, "Smart Shuffle Liked", public=False)
            target_pl_id = new_pl['id']
            # Para Liked Songs no usamos replace_items sino add_items
            first_batch = uris[:100]
            sp.playlist_add_items(target_pl_id, first_batch)
            start_idx = 100
        else:
            target_pl_id = pl_id
            # Usamos replace_items porque es más eficiente para limpiar y rellenar
            sp.playlist_replace_items(target_pl_id, uris[:100])
            start_idx = 100

        with tqdm(total=len(uris), desc="Actualizando Spotify", unit="track") as pbar:
            pbar.update(min(100, len(uris)))
            for i in range(start_idx, len(uris), 100):
                batch = uris[i:i+100]
                sp.playlist_add_items(target_pl_id, batch)
                pbar.update(len(batch))
        
        print(f"✅ ¡Hecho! La playlist ha sido mezclada.")
        
        otra = input("\n¿Quieres mezclar otra playlist? (s/n): ").strip().lower()
        if otra != 's': break

if __name__ == "__main__":
    main()
