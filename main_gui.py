import customtkinter as ctk
import os
import sys
import subprocess
import threading
import time
import runpy
import io
from PIL import Image
from dotenv import load_dotenv

# --- CORRECCIÓN DE CODIFICACIÓN PARA EMOJIS EN WINDOWS ---
if sys.stdout is not None and sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Para versiones de Python muy antiguas o entornos raros
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.dirname(__file__))

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- SISTEMA DE CREDENCIALES PLUG & PLAY ---
load_dotenv() # [CREDENTIALS_MARKER]

def check_credentials():
    return all([os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET'), os.getenv('SPOTIFY_REDIRECT_URI')])

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class SpotifyToolkitApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Spotify Toolkit v1.0 - Premium")
        self.geometry("1000x800")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.font_title = ctk.CTkFont(family="Inter", size=24, weight="bold")
        self.font_subtitle = ctk.CTkFont(family="Inter", size=14)
        
        self.current_process = None

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="🎵 Toolkit", font=self.font_title)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Inicio", command=self.show_home, fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"))
        self.home_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.clean_button = ctk.CTkButton(self.sidebar_frame, text="Limpieza", command=self.show_clean, fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"))
        self.clean_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.organize_button = ctk.CTkButton(self.sidebar_frame, text="Organizar", command=self.show_organize, fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"))
        self.organize_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.stats_button = ctk.CTkButton(self.sidebar_frame, text="Estadísticas", command=self.show_stats, fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"))
        self.stats_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # Main Container
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1) 
        self.main_frame.grid_rowconfigure(1, weight=0) 

        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Log Area
        self.log_container = ctk.CTkFrame(self.main_frame)
        self.log_container.grid(row=1, column=0, sticky="ew", pady=(20, 0))
        self.log_container.grid_columnconfigure(0, weight=1)

        self.log_textbox = ctk.CTkTextbox(self.log_container, height=250, font=("Consolas", 12))
        self.log_textbox.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        
        # Input Frame (para interactuar con los scripts)
        self.input_frame = ctk.CTkFrame(self.log_container, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.command_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Escribir aquí...", height=35)
        self.command_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.command_entry.bind("<Return>", lambda e: self.send_input_to_script())

        self.send_button = ctk.CTkButton(self.input_frame, text="Enviar", width=100, command=self.send_input_to_script, state="disabled")
        self.send_button.grid(row=0, column=1)

        if check_credentials():
            self.add_log("✅ Sistema listo para rockear")
        else:
            self.add_log("❌ Error fatal: Credenciales no encontradas")

        self.show_home()

    def add_log(self, text):
        self.log_textbox.insert("end", text + "\n")
        self.log_textbox.see("end")

    def send_input_to_script(self):
        if self.current_process and self.current_process.poll() is None:
            cmd = self.command_entry.get()
            if cmd:
                try:
                    self.current_process.stdin.write(cmd + "\n")
                    self.current_process.stdin.flush()
                    self.add_log(f"> {cmd}")
                    self.command_entry.delete(0, "end")
                except Exception as e:
                    self.add_log(f"❌ Error enviando comando: {e}")

    def run_script_thread(self, script_path):
        if self.current_process and self.current_process.poll() is None:
            self.add_log("\n⚠️ Ya hay una herramienta en ejecución. Espere a que termine o cierre la App.")
            return

        def run():
            self.send_button.configure(state="normal")
            abs_script_path = get_resource_path(script_path)
            self.add_log(f"\n🚀 Iniciando: {os.path.basename(script_path)}")
            
            try:
                env = os.environ.copy()
                env['PYTHONIOENCODING'] = 'utf-8'
                env['PYTHONUNBUFFERED'] = "1"
                env['SPOTIPY_CLIENT_ID'] = os.getenv('SPOTIFY_CLIENT_ID', '')
                env['SPOTIPY_CLIENT_SECRET'] = os.getenv('SPOTIFY_CLIENT_SECRET', '')
                env['SPOTIPY_REDIRECT_URI'] = os.getenv('SPOTIFY_REDIRECT_URI', '')

                self.current_process = subprocess.Popen(
                    [sys.executable, "--run", abs_script_path],
                    env=env,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    bufsize=1,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )

                while True:
                    line = self.current_process.stdout.readline()
                    if not line and self.current_process.poll() is not None:
                        break
                    if line:
                        self.add_log(line.strip())
                
                self.current_process.wait()
            except Exception as e:
                self.add_log(f"❌ Error en proceso: {e}")
            
            self.add_log(f"✅ Proceso terminado")
            self.send_button.configure(state="disabled")
            self.current_process = None

        threading.Thread(target=run, daemon=True).start()

    def state_buttons(self, state):
        # Mantener botones laterales siempre activos para navegación
        pass

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Spotify Toolkit Premium", font=self.font_title).grid(row=0, column=0, pady=(0, 10), sticky="w")
        ctk.CTkLabel(self.content_frame, text="Tus herramientas están listas. Elige una del menú lateral.", font=self.font_subtitle).grid(row=1, column=0, sticky="nw")

    def show_clean(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Limpieza profunda", font=self.font_title).grid(row=0, column=0, pady=(0, 20), sticky="w")
        ctk.CTkButton(self.content_frame, text="Borrar Duplicados", height=45, width=220, command=lambda: self.run_script_thread("Delet Duplicates/delet_duplicates.py")).grid(row=1, column=0, pady=10, sticky="w")

    def show_organize(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Organización", font=self.font_title).grid(row=0, column=0, pady=(0, 20), sticky="w")
        tools = [
            ("Separar por Géneros", "Separate Genres/Separate Genres.py"),
            ("Separar por Artistas", "Separate Artists/Separate Artists.py"),
            ("Reordenar Playlist", "Reorder/reorder.py"),
            ("Extraer Artistas", "Extraer Artistas/Extraer Artistas.py")
        ]
        for i, (name, path) in enumerate(tools):
            ctk.CTkButton(self.content_frame, text=name, height=45, width=220, command=lambda p=path: self.run_script_thread(p)).grid(row=i+1, column=0, pady=5, sticky="w")

    def show_stats(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Estadísticas y Mezcla", font=self.font_title).grid(row=0, column=0, pady=(0, 20), sticky="w")
        ctk.CTkButton(self.content_frame, text="Top Canciones", height=45, width=220, command=lambda: self.run_script_thread("Top Tracks/TopTracks.py")).grid(row=1, column=0, pady=10, sticky="w")
        ctk.CTkButton(self.content_frame, text="Smart Shuffle", height=45, width=220, command=lambda: self.run_script_thread("Shufle/Shufle.py")).grid(row=2, column=0, pady=10, sticky="w")

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--run":
        target_script = sys.argv[2]
        if os.path.exists(target_script):
            os.chdir(os.path.dirname(target_script))
            if hasattr(sys, '_MEIPASS'):
                sys.path.append(sys._MEIPASS)
            try:
                # FORZAMOS UTF-8 TAMBIÉN AL EJECUTAR EL SCRIPT INTERNO
                runpy.run_path(target_script, run_name="__main__")
            except Exception as e:
                print(f"\n❌ Error fatal en script: {e}")
        sys.exit()
    else:
        app = SpotifyToolkitApp()
        app.mainloop()
