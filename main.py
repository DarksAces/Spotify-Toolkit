import customtkinter as ctk
import os
import sys
import subprocess
import threading
import time
import runpy
import io
import difflib # Forzamos la inclusión para PyInstaller
import locale
import re
from PIL import Image
from dotenv import load_dotenv
import tqdm
import spotipy

# --- CORRECCIÓN DE CODIFICACIÓN PARA EMOJIS EN WINDOWS ---
if sys.stdout is not None and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

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

# --- INTERNATIONALIZATION (i18n) ---
def get_system_lang():
    try:
        lang = locale.getlocale()[0]
        if lang and lang.lower().startswith('es'):
            return 'es'
    except:
        pass
    return 'en'

LANG = get_system_lang()

TEXTS = {
    'es': {
        'title': "Spotify Toolkit v1.0.8",
        'sidebar_home': "Inicio",
        'sidebar_clean': "Limpieza",
        'sidebar_organize': "Organizar",
        'sidebar_stats': "Estadísticas",
        'ready': "✅ Sistema listo",
        'no_creds': "⚠️ Credenciales no encontradas (.env)",
        'welcome_title': "Spotify Toolkit",
        'welcome_desc': "Tus herramientas están listas. Elige una del menú lateral.",
        'clean_title': "Limpieza profunda",
        'organize_title': "Organización",
        'stats_title': "Estadísticas y Mezcla",
        'btn_delete_duplicates': "Borrar Duplicados",
        'desc_delete_duplicates': "Busca e elimina canciones repetidas.",
        'btn_separate_genres': "Separar por Géneros",
        'desc_separate_genres': "Crea listas separadas por géneros.",
        'btn_separate_artists': "Separar por Artistas",
        'desc_separate_artists': "Playlists individuales por artista.",
        'btn_reorder_tracks': "Mover Artista al Final",
        'desc_reorder_tracks': "Mueve un artista específico al final.",
        'btn_trend_reports': "Informe de Tendencias",
        'desc_trend_reports': "Informe de tus géneros más escuchados.",
        'btn_artist_extractor': "Extraer Artistas",
        'desc_artist_extractor': "Lista de artistas en una playlist.",
        'btn_playlist_time': "Duración Playlist",
        'desc_playlist_time': "Calcula el tiempo total exacto.",
        'btn_top_tracks': "Top Canciones",
        'desc_top_tracks': "Tus canciones más escuchadas.",
        'btn_smart_shuffle': "Smart Shuffle",
        'desc_smart_shuffle': "Mezcla evitando artistas seguidos.",
        'btn_metadata_export': "Exportar Metadatos",
        'desc_metadata_export': "Exporta una playlist a CSV o JSON.",
        'input_placeholder': "Escribir aquí...",
        'btn_send': "Enviar",
        'btn_cancel': "Cancelar",
        'running': "\n🚀 Iniciando:",
        'finished': "\n✅ Proceso terminado",
        'cancelled': "\n🛑 Proceso cancelado.",
        'already_running': "\n⚠️ Ya hay una herramienta en ejecución.",
        'error_input': "❌ Error al enviar input: ",
        'error_fatal': "❌ Error fatal en script: "
    },
    'en': {
        'title': "Spotify Toolkit v1.0.8",
        'sidebar_home': "Home",
        'sidebar_clean': "Clean",
        'sidebar_organize': "Organize",
        'sidebar_stats': "Statistics",
        'ready': "✅ System ready",
        'no_creds': "⚠️ Credentials not found (.env)",
        'welcome_title': "Spotify Toolkit",
        'welcome_desc': "Your tools are ready. Choose one from the sidebar.",
        'clean_title': "Deep Cleaning",
        'organize_title': "Organization",
        'stats_title': "Stats & Mixing",
        'btn_delete_duplicates': "Delete Duplicates",
        'desc_delete_duplicates': "Find and remove repeated songs.",
        'btn_separate_genres': "Separate by Genres",
        'desc_separate_genres': "Create separate lists by genre.",
        'btn_separate_artists': "Separate by Artists",
        'desc_separate_artists': "Individual playlists per artist.",
        'btn_reorder_tracks': "Move Artist to End",
        'desc_reorder_tracks': "Move specific artist to the end.",
        'btn_trend_reports': "Trend Reports",
        'desc_trend_reports': "Report of your top genres.",
        'btn_artist_extractor': "Extract Artists",
        'desc_artist_extractor': "List of artists in a playlist.",
        'btn_playlist_time': "Playlist Duration",
        'desc_playlist_time': "Calculate exact playback time.",
        'btn_top_tracks': "Top Tracks",
        'desc_top_tracks': "Your most listened tracks.",
        'btn_smart_shuffle': "Smart Shuffle",
        'desc_smart_shuffle': "Shuffle avoiding repeated artists.",
        'btn_metadata_export': "Export Metadata",
        'desc_metadata_export': "Export to CSV or JSON.",
        'input_placeholder': "Type here...",
        'btn_send': "Send",
        'btn_cancel': "Cancel",
        'running': "\n🚀 Starting:",
        'finished': "\n✅ Process finished",
        'cancelled': "\n🛑 Process cancelled.",
        'already_running': "\n⚠️ Another tool is already running.",
        'error_input': "❌ Error sending input: ",
        'error_fatal': "❌ Fatal error in script: "
    }
}

T = TEXTS[LANG]

# --- SISTEMA DE CREDENCIALES PLUG & PLAY ---
load_dotenv() # [CREDENTIALS_MARKER]

def check_credentials():
    return all([os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET'), os.getenv('SPOTIFY_REDIRECT_URI')])

ctk.set_appearance_mode("dark")

class SpotifyToolkitApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(T['title'])
        self.geometry("1000x850")

        # Official Spotify Hex Palette
        self.bg_color = "#121212"      # Main content background
        self.sidebar_color = "#000000" # True black sidebar
        self.accent_color = "#1DB954"  # Spotify Green
        self.hover_color = "#1ed760"    # Lighter Green
        self.text_color = "#FFFFFF"
        self.subtext_color = "#B3B3B3"
        self.card_color = "#181818"    # Subtle card background

        self.configure(fg_color=self.bg_color)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.font_title = ctk.CTkFont(family="Inter", size=32, weight="bold")
        self.font_sidebar = ctk.CTkFont(family="Inter", size=14, weight="bold")
        self.font_subtitle = ctk.CTkFont(family="Inter", size=16, weight="bold")
        self.font_desc = ctk.CTkFont(family="Inter", size=13)
        
        self.current_process = None

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=self.sidebar_color)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Toolkit", font=ctk.CTkFont(size=26, weight="bold"), text_color=self.text_color)
        self.logo_label.grid(row=0, column=0, padx=25, pady=(40, 30), sticky="w")

        # Utility to create buttons with consistent spacing
        def make_nav_btn(text, cmd, row):
            btn = ctk.CTkButton(self.sidebar_frame, text=text, command=cmd, 
                                fg_color="transparent", text_color=self.subtext_color, 
                                hover_color="#282828", anchor="w", 
                                font=self.font_sidebar, height=45, corner_radius=8)
            btn.grid(row=row, column=0, padx=10, pady=2, sticky="ew")
            return btn

        self.home_button = make_nav_btn("  🏠  " + T['sidebar_home'], self.show_home, 1)
        self.clean_button = make_nav_btn("  ✨  " + T['sidebar_clean'], self.show_clean, 2)
        self.organize_button = make_nav_btn("  📁  " + T['sidebar_organize'], self.show_organize, 3)
        self.stats_button = make_nav_btn("  📊  " + T['sidebar_stats'], self.show_stats, 4)

        # Main Container
        self.main_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.main_frame.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1) 
        self.main_frame.grid_rowconfigure(1, weight=0) 

        self.content_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Log Area
        self.log_container = ctk.CTkFrame(self.main_frame, fg_color="#181818", corner_radius=10)
        self.log_container.grid(row=1, column=0, sticky="ew", pady=(20, 0))
        self.log_container.grid_columnconfigure(0, weight=1)

        self.log_textbox = ctk.CTkTextbox(self.log_container, height=280, font=("Consolas", 12), state="disabled", fg_color="transparent", text_color="#E0E0E0")
        self.log_textbox.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="ew")
        
        # Configure color tags
        self.log_textbox.tag_config("success", foreground="#1DB954") # Spotify Green
        self.log_textbox.tag_config("error", foreground="#FF4B4B")   # Soft Red
        self.log_textbox.tag_config("warning", foreground="#FFD700") # Gold
        self.log_textbox.tag_config("info", foreground="#53B2FF")    # Bright Blue
        
        self.input_frame = ctk.CTkFrame(self.log_container, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.command_entry = ctk.CTkEntry(self.input_frame, placeholder_text=T['input_placeholder'], height=40, corner_radius=20, border_color="#333333", fg_color="#2A2A2A")
        self.command_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.command_entry.bind("<Return>", lambda e: self.send_input_to_script())

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.log_container, height=6, corner_radius=3, progress_color=self.accent_color, fg_color="#333333")
        self.progress_bar.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="ew")
        self.progress_bar.set(0)

        self.send_button = ctk.CTkButton(self.input_frame, text=T['btn_send'], width=100, corner_radius=20, command=self.send_input_to_script, state="disabled", fg_color=self.accent_color, hover_color=self.hover_color, text_color="#000000", font=ctk.CTkFont(weight="bold"))
        self.send_button.grid(row=0, column=1)

        self.stop_button = ctk.CTkButton(self.input_frame, text=T['btn_cancel'], width=100, corner_radius=20, fg_color="#333333", hover_color="#444444", command=self.stop_current_process, state="disabled", font=ctk.CTkFont(weight="bold"))
        self.stop_button.grid(row=0, column=2, padx=(10, 0))

        if check_credentials():
            self.add_log(T['ready'])
        else:
            self.add_log(T['no_creds'])

        self.show_home()

    def add_log(self, text):
        def _append():
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", text + "\n")
            self.log_textbox.configure(state="disabled")
            self.log_textbox.see("end")
        self.after(0, _append)

    def add_log_raw(self, text):
        def _append():
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", text)
            self.log_textbox.configure(state="disabled")
            self.log_textbox.see("end")
        self.after(0, _append)

    def send_input_to_script(self):
        if self.current_process and self.current_process.poll() is None:
            cmd = self.command_entry.get()
            try:
                self.current_process.stdin.write(cmd + "\n")
                self.current_process.stdin.flush()
                self.add_log(f"> {cmd}")
                self.command_entry.delete(0, "end")
            except Exception as e:
                self.add_log(f"{T['error_input']}{e}")

    def stop_current_process(self):
        if self.current_process and self.current_process.poll() is None:
            self.current_process.terminate()
            self.add_log(T['cancelled'])

    def run_script_thread(self, script_path):
        if self.current_process and self.current_process.poll() is None:
            self.add_log(T['already_running'])
            return

        def run():
            self.send_button.configure(state="normal")
            self.stop_button.configure(state="normal")
            self.command_entry.focus()
            self.progress_bar.set(0)
            abs_script_path = get_resource_path(script_path)
            self.add_log(f"{T['running']} {os.path.basename(script_path)}")
            
            try:
                env = os.environ.copy()
                env['PYTHONIOENCODING'] = 'utf-8'
                env['PYTHONUNBUFFERED'] = "1"

                if hasattr(sys, '_MEIPASS'):
                    cmd = [sys.executable, "--run", abs_script_path]
                else:
                    cmd = [sys.executable, sys.argv[0], "--run", abs_script_path]

                self.current_process = subprocess.Popen(
                    cmd, env=env, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding='utf-8', errors='replace', bufsize=0,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )

                while True:
                    char = self.current_process.stdout.read(1)
                    if not char:
                        if self.current_process.poll() is not None:
                            break
                        continue
                    self.add_log_raw(char)
                
                self.current_process.wait()

            except Exception as e:
                self.add_log(f"❌ Error crítico: {e}")
            
            self.add_log(T['finished'])
            self.send_button.configure(state="disabled")
            self.stop_button.configure(state="disabled")
            self.current_process = None

        threading.Thread(target=run, daemon=True).start()

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text=T['welcome_title'], font=self.font_title, text_color=self.text_color).grid(row=0, column=0, pady=(0, 10), sticky="w")
        ctk.CTkLabel(self.content_frame, text=T['welcome_desc'], font=self.font_subtitle, text_color=self.subtext_color).grid(row=1, column=0, sticky="nw")

    def add_tool_button(self, name, desc, path, row):
        btn = ctk.CTkButton(self.content_frame, text=name, height=40, width=220, command=lambda: self.run_script_thread(path))
        btn.grid(row=row*2, column=0, pady=(10, 0), sticky="w")
        lbl = ctk.CTkLabel(self.content_frame, text=desc, font=self.font_desc, text_color="gray70")
        lbl.grid(row=row*2+1, column=0, padx=(5, 0), pady=(0, 10), sticky="w")

    def show_clean(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text=T['clean_title'], font=self.font_title).grid(row=0, column=0, pady=(0, 20), sticky="w")
        self.add_tool_button(T['btn_delete_duplicates'], T['desc_delete_duplicates'], "delete_duplicates/delete_duplicates.py", 1)

    def show_organize(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text=T['organize_title'], font=self.font_title, text_color=self.text_color).grid(row=0, column=0, pady=(0, 20), sticky="w")
        tools = [
            (T['btn_separate_genres'], T['desc_separate_genres'], "separate_genres/separate_genres.py"),
            (T['btn_separate_artists'], T['desc_separate_artists'], "separate_artists/separate_artists.py"),
            (T['btn_reorder_tracks'], T['desc_reorder_tracks'], "reorder_tracks/reorder_tracks.py"),
            (T['btn_artist_extractor'], T['desc_artist_extractor'], "artist_extractor/artist_extractor.py"),
            (T['btn_playlist_time'], T['desc_playlist_time'], "playlist_time/playlist_time.py"),
            (T['btn_metadata_export'], T['desc_metadata_export'], "metadata_export/metadata_export.py")
        ]
        for i, (name, desc, path) in enumerate(tools):
            self.add_tool_button(name, desc, path, i+1)

    def show_stats(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text=T['stats_title'], font=self.font_title, text_color=self.text_color).grid(row=0, column=0, pady=(0, 20), sticky="w")
        self.add_tool_button(T['btn_top_tracks'], T['desc_top_tracks'], "top_tracks_generator/top_tracks_generator.py", 1)
        self.add_tool_button(T['btn_trend_reports'], T['desc_trend_reports'], "trend_reports/trend_reports.py", 2)
        self.add_tool_button(T['btn_smart_shuffle'], T['desc_smart_shuffle'], "smart_shuffle/smart_shuffle.py", 3)

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--run":
        target_script = sys.argv[2]
        if os.path.exists(target_script):
            os.chdir(os.path.dirname(target_script))
            if hasattr(sys, '_MEIPASS'):
                sys.path.append(sys._MEIPASS)
            try:
                runpy.run_path(target_script, run_name="__main__")
            except Exception as e:
                print(f"{T['error_fatal']}{e}")
        sys.exit()
    else:
        app = SpotifyToolkitApp()
        app.mainloop()
