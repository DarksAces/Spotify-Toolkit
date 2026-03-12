import os
import sys
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    scripts = {
        "1": ("Delet Duplicates", "Delet Duplicates/delet_duplicates.py"),
        "2": ("Extraer Artistas", "Extraer Artistas/Extraer Artistas.py"),
        "3": ("Separate Genres", "Separate Genres/Separate Genres.py"),
        "4": ("Separate Artists", "Separate Artists/Separate Artists.py"),
        "5": ("Top Tracks", "Top Tracks/TopTracks.py"),
        "6": ("Shuffle", "Shufle/Shufle.py"),
        "7": ("Playlist Duration (Time)", "Time/timer.py"),
        "8": ("Reorder Tracks", "Reorder/reorder.py")
    }

    while True:
        clear_screen()
        print("="*50)
        print("🎵  SPOTIFY TOOLKIT - ALL-IN-ONE  🎵")
        print("="*50)
        print("\nElige una herramienta para ejecutar:")
        
        # We will dynamically find scripts if possible, but for the EXE we use the mapping
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
                 # Try to find it if path naming is slightly different
                 print(f"❌ No se encontró el script en: {path}")
                 input("\nPresiona Enter para volver...")
                 continue

            print(f"\n🚀 Iniciando: {name}...\n")
            try:
                # Run the script as a subprocess so it doesn't kill the main menu
                subprocess.run([sys.executable, full_path], check=True)
            except Exception as e:
                print(f"❌ Error al ejecutar el script: {e}")
            
            input("\n✅ Proceso terminado. Presiona Enter para volver al menú...")
        else:
            print("❌ Opción no válida.")
            time.sleep(1)

if __name__ == "__main__":
    # Check if .env exists, if not warn the user
    if not os.path.exists(".env") and not os.getenv("SPOTIFY_CLIENT_ID"):
        print("⚠️  ADVERTENCIA: No se encontró el archivo .env")
        print("Asegúrate de configurar tus credenciales de Spotify API.")
        input("\nPresiona Enter para continuar de todos modos...")
    
    main_menu()
