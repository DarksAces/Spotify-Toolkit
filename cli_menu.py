import os
import sys
import subprocess
import time
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    scripts = {
        "1": ("Delete Duplicates", "delete_duplicates/delete_duplicates.py"),
        "2": ("Artist Extractor", "artist_extractor/artist_extractor.py"),
        "3": ("Separate Genres", "separate_genres/separate_genres.py"),
        "4": ("Separate Artists", "separate_artists/separate_artists.py"),
        "5": ("Top Tracks Generator", "top_tracks_generator/top_tracks_generator.py"),
        "6": ("Smart Shuffle", "smart_shuffle/smart_shuffle.py"),
        "7": ("Playlist Duration (Time)", "playlist_time/playlist_time.py"),
        "8": ("Reorder Tracks", "reorder_tracks/reorder_tracks.py"),
        "9": ("Mood Mixer", "mood_mixer/mood_mixer.py")
    }

    while True:
        clear_screen()
        print("="*50)
        print("🎵  SPOTIFY TOOLKIT - CLI MENU  🎵")
        print("="*50)
        print("\nElige una herramienta para ejecutar:")
        
        for key, (name, path) in scripts.items():
            print(f"{key}. {name}")
        
        print("Q. Salir")
        print("\n" + "="*50)
        
        choice = input("\n> ").strip().upper()
        
        if choice == 'Q':
            print("¡Hasta luego! 🎶")
            break
        
        if choice in scripts:
            name, path = scripts[choice]
            full_path = os.path.join(os.path.dirname(__file__), path)
            
            if not os.path.exists(full_path):
                 print(f"❌ No se encontró el script en: {path}")
                 input("\nPresiona Enter para volver...")
                 continue

            print(f"\n🚀 Iniciando: {name}...\n")
            try:
                subprocess.run([sys.executable, full_path], check=True)
            except Exception as e:
                print(f"❌ Error al ejecutar el script: {e}")
            
            input("\n✅ Proceso terminado. Presiona Enter para volver al menú...")
        else:
            print("❌ Opción no válida.")
            time.sleep(1)

if __name__ == "__main__":
    if not os.path.exists(".env") and not os.getenv("SPOTIFY_CLIENT_ID"):
        print("⚠️  ADVERTENCIA: No se encontró el archivo .env")
        print("Asegúrate de configurar tus credenciales de Spotify API.")
        input("\nPresiona Enter para continuar de todos modos...")
    
    main_menu()
