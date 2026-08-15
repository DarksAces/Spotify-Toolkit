# 🎵 Spotify Toolkit

![GitHub release](https://img.shields.io/github/v/release/DarksAces/Spotify-Toolkit?style=for-the-badge&color=1DB954)
![GitHub stars](https://img.shields.io/github/stars/DarksAces/Spotify-Toolkit?style=for-the-badge&color=white)
![Python Version](https://img.shields.io/badge/python-3.9+-yellow?style=for-the-badge&logo=python)
![GitHub Discussions](https://img.shields.io/github/discussions/DarksAces/Spotify-Toolkit?style=for-the-badge&color=89dceb&label=Community&logo=github)
![GitHub license](https://img.shields.io/github/license/DarksAces/Spotify-Toolkit?style=for-the-badge&color=1DB954)

A powerful, all-in-one GUI suite designed to manage, clean, and optimize your Spotify library with ease. Leverage the full power of the Spotify API through a friendly and intuitive interface.

---

## 🇺🇸 English Version

### 🚀 Quick Start (Plug & Play)

1.  **Download:** Get the latest `SpotifyToolkit.exe` from the [Releases](https://github.com/DarksAces/Spotify-Toolkit/releases) section.
2.  **No Setup Required:** The official executable is pre-configured. You **don't** need to create a Spotify Developer account or deal with Client IDs.
3.  **🛡️ Security Note:** > [!IMPORTANT]
    > As an Open Source project without a paid digital signature, Windows SmartScreen might flag the file. This is a **False Positive**.
    > - **Browser:** Select "Keep" or "Download anyway".
    > - **Windows:** Click "More info" → **"Run anyway"**.

### ✨ Key Features
* **🌍 Smart i18n:** Automatic interface switching between English and Spanish.
* **🖱️ Modern GUI:** Integrated interactive console—no more external terminal windows.
* **🔍 Instant Search:** Filter and find your playlists instantly by typing their names.
* **⚡ Live Control:** Real-time logging and an instant **Cancel** button to stop any process.
* **📦 Modular Tools:** Duplicate removal, library stats, smart shuffling, and more.

### 📖 How to Use
1.  Launch `SpotifyToolkit.exe`.
2.  Choose a tool from the sidebar.
3.  Interact using the **bottom input bar** and press **Enter**.
4.  Authorize via your browser (one-time setup).

---

## 🇪🇸 Versión en Español

### 🚀 Inicio Rápido (Plug & Play)

1.  **Descarga:** Consigue el último `SpotifyToolkit.exe` en la sección de [Releases](https://github.com/DarksAces/Spotify-Toolkit/releases).
2.  **Sin Configuración:** El ejecutable oficial ya viene configurado. **No** necesitas crear una cuenta de desarrollador ni configurar Client IDs.
3.  **🛡️ Nota de Seguridad:**
    > [!IMPORTANT]
    > Al ser un proyecto Open Source sin firma digital de pago, Windows SmartScreen podría marcarlo. Es un **Falso Positivo**.
    > - **Navegador:** Elige "Conservar" o "Descargar de todos modos".
    > - **Windows:** Haz clic en "Más información" → **"Ejecutar de todos modos"**.

### ✨ Características Principales
* **🌍 Idioma Automático:** Interfaz dual (Inglés/Español) según la configuración de tu sistema.
* **🖱️ Interfaz Moderna:** Consola interactiva integrada; olvida las ventanas de terminal externas.
* **🔍 Búsqueda Inteligente:** Filtra y selecciona tus playlists al instante escribiendo su nombre.
* **⚡ Control en Vivo:** Visualiza el progreso en tiempo real y detén procesos con el botón **Cancelar**.
* **📦 Herramientas Modulares:** Limpieza de duplicados, estadísticas, Smart Shuffle y más.

### 📖 Modo de Uso
1.  Inicia `SpotifyToolkit.exe`.
2.  Selecciona una herramienta en el menú lateral.
3.  Usa la **barra de entrada inferior** para interactuar y pulsa **Enter**.
4.  Inicia sesión en el navegador cuando se te solicite (solo la primera vez).

---

## 🛠️ For Developers / Para Desarrolladores

### Run from source:
```bash
git clone https://github.com/DarksAces/Spotify-Toolkit.git
cd Spotify-Toolkit
pip install -r requirements.txt
# Copy .env.example to .env and fill in your Client ID
python main.py
```

## 🧠 Architecture / Arquitectura

* **Secure Auth (PKCE):** The app uses the **Authorization Code with PKCE** flow (no client secret required). Each user authorises their own Spotify account through the browser. Only the `SPOTIFY_CLIENT_ID` is distributed — it is not a secret and cannot be used alone to make API calls on behalf of another user.
* **Token Cache:** The OAuth token is stored in the current user's OS application-data directory (`%APPDATA%\SpotifyToolkit\` on Windows), never in the project root or a shared location.
* **Async Execution:** All tools run on **separate threads** using Python's `threading` module to prevent the GUI from freezing during long-running API operations.
* **Standardized I/O:** A custom engine routes `stdout` directly to the UI's internal console and redirects user `stdin` via the integrated input bar.

---

## 🤝 Community & Support

Join our community to help shape the future of **Spotify Toolkit**! 

* **🙋 [Questions & Help](https://github.com/DarksAces/Spotify-Toolkit/discussions/categories/q-a)** – Stuck with something? Ask the community for a hand.
* **💡 [Feature Requests](https://github.com/DarksAces/Spotify-Toolkit/discussions/categories/ideas)** – Have a cool idea? Suggest it here and let others vote.
* **🚀 [Show & Tell](https://github.com/DarksAces/Spotify-Toolkit/discussions/categories/show-and-tell)** – Share how you are using the toolkit or show off your curated playlists!
* **🐛 [Bug Reports](https://github.com/DarksAces/Spotify-Toolkit/issues)** – Found a technical issue? Open a formal ticket so we can fix it.

---

*Distributed under the **MIT License**. Developed with ❤️ for music lovers.*
