# 🎵 Spotify Toolkit

![GitHub release (latest by date)](https://img.shields.io/github/v/release/DarksAces/Spotify-Toolkit?style=for-the-badge&color=1DB954)
![GitHub Repo stars](https://img.shields.io/github/stars/DarksAces/Spotify-Toolkit?style=for-the-badge&color=white)
![GitHub license](https://img.shields.io/github/license/DarksAces/Spotify-Toolkit?style=for-the-badge&color=1DB954)
![Python Version](https://img.shields.io/badge/python-3.9+-yellow?style=for-the-badge&logo=python)

---

# 🇺🇸 English Version

A powerful collection of GUI tools to manage, clean, and enhance your Spotify experience. This toolkit uses the Spotify API to give you full control over your playlists, liked songs, and library statistics.

## 🚀 Download & Security (Plug & Play)

### 1. Download
Go to the **Releases** section on the right and download the latest `SpotifyToolkit.exe`.

### 2. 🛡️ Security Warning (False Positive)
> [!IMPORTANT]
> **Why does Windows say it's not safe?**
> This tool is Open Source and created with PyInstaller. Since it doesn't have a paid digital signature (which costs hundreds of dollars), Windows SmartScreen and browsers may flag it as "unrecognized" or "dangerous".
> 
> **It is a False Positive.** You can run it safely:
> 1. **Browser:** Choose "Keep" or "Download anyway".
> 2. **Windows (Blue Screen):** Click **"More info"** and then **"Run anyway"**.

### 3. ✅ Pre-configured (No Setup Required)
> [!TIP]
> **The executable is "Plug & Play".** You do **NOT** need to create a Spotify Dev account or enter your own credentials (Client ID/Secret) if you use the official release. It comes pre-configured and ready to use!

## ✨ Key Features
- **Integrated Interactive Console:** No more messy terminal windows. Everything happens inside the app.
- **Fuzzy Matching Search:** Typing "The Beatles" without accents or "Beatls" by mistake? The app will suggest the closest match.
- **Live Process Control:** Change of heart? Use the **Cancel** button to stop any running script immediately.
- **Automatic Discovery:** The app automatically lists all your playlists for easy selection.
- **Background Tasks:** Keep browsing the app's tabs while a tool is working in the background.

## 📖 Usage
1. Open `SpotifyToolkit.exe`.
2. Select the tool you want to use from the sidebar.
3. If a tool needs your input (like choosing a playlist), **type it in the bottom input bar** of the app and press **Enter**.
4. Log in to Spotify in the browser window if prompted (only required the first time).

---

# 🇪🇸 Versión en Español

Una colección potente de herramientas con interfaz gráfica para gestionar, limpiar y potenciar tu experiencia en Spotify. Este toolkit utiliza la API de Spotify para darte control total sobre tus playlists, canciones favoritas y estadísticas.

## 🚀 Descarga y Seguridad (Plug & Play)

### 1. Descarga
Ve a la sección de **Releases** a la derecha y descarga el último `SpotifyToolkit.exe`.

### 2. 🛡️ Aviso de Seguridad (Falso Positivo)
> [!IMPORTANT]
> **¿Por qué Windows dice que no es seguro?**
> Esta herramienta es de código abierto y está creada con PyInstaller. Al no tener una firma digital de pago (que cuesta cientos de euros), Windows SmartScreen y los navegadores pueden marcarlo como "desconocido" o "peligroso".
> 
> **Es un Falso Positivo.** Puedes usarlo con total seguridad:
> 1. **Navegador:** Elige "Conservar" o "Descargar de todos modos".
> 2. **Windows (Pantalla Azul):** Haz clic en **"Más información"** y luego en **"Ejecutar de todos modos"**.

### 3. ✅ Ya configurado (Sin configuración manual)
> [!TIP]
> **El ejecutable es "Plug & Play".** **NO** es necesario que crees una cuenta de desarrollador de Spotify ni que pongas tus propias credenciales (Client ID/Secret) si usas la versión oficial. ¡Viene ya configurado y listo para usar!

## ✨ Características Principales
- **Consola Interactiva Integrada:** Se acabaron las ventanas negras de terminal. Todo ocurre dentro de la aplicación.
- **Búsqueda con "Fuzzy Matching":** ¿Escribiste "The Beatles" sin tildes o "Beatls" por error? La app te sugerirá la coincidencia más cercana.
- **Control de Procesos en Vivo:** ¿Te arrepentiste? Usa el botón **Cancelar** para detener cualquier script al instante.
- **Descubrimiento Automático:** La app lista todas tus playlists automáticamente para que solo tengas que elegir un número.
- **Navegación Fluida:** Sigue explorando las pestañas de la app mientras una herramienta trabaja de fondo.

## 📖 Uso
1. Abre `SpotifyToolkit.exe`.
2. Selecciona la herramienta que quieras usar en el menú lateral.
3. Si la herramienta necesita que escribas algo (como elegir una playlist), **escríbelo en la barra inferior** de la app y pulsa **Enter**.
4. Inicia sesión en Spotify en el navegador si se te solicita (solo la primera vez).

---

## 🛠️ For Developers / Para Desarrolladores

### Run from source (Manual Setup):
1. Clone the repo.
2. Install dependencies: `pip install spotipy python-dotenv customtkinter pillow`.
3. Create a `.env` file with your `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, and `SPOTIFY_REDIRECT_URI`.
4. Run `python main_gui.py`.

## 🧠 Code Architecture / Arquitectura del Código

### 1. **Credential Injection (GitHub Actions)**
The most important part of the automation. The `build.yml` workflow takes GitHub Secrets and physically injects them into `main_gui.py` during the build process. This is what allows the "Plug & Play" experience without exposing keys in the public source code.

### 2. **Interactive Threading System**
To prevent the GUI from freezing, every tool runs in a separate **thread**. 
- The main GUI sends credentials through **Environment Variables**.
- It features **bidirectional communication**: captures script output and sends user input from the GUI directly to the script's `stdin`.
- Includes a process termination handler linked to the **Cancel** button.

### 3. **Smart Resource Management**
The project uses a custom `get_resource_path()` function to handle file paths. This ensures that icons and sub-scripts are found correctly whether you are running the raw `.py` file or the compiled `.exe`.

---

### **1. Inyección de Credenciales (GitHub Actions)**
La parte más clave de la automatización. El workflow `build.yml` toma los Secrets de GitHub y los inyecta físicamente en el código de `main_gui.py` durante el proceso de compilación. Esto es lo que permite la experiencia "Plug & Play" sin exponer tus claves en el código fuente público.

### 2. **Sistema de Hilos Interactivo**
Para evitar que la interfaz se congele, cada herramienta se ejecuta en un **hilo (thread)** separado.
- La interfaz principal pasa las credenciales inyectadas mediante **Variables de Entorno**.
- Permite **comunicación bidireccional**: captura la salida de los scripts y envía lo que escribas en la GUI directamente al `stdin` del script hijo.
- Incluye un gestor de terminación conectado al botón **Cancelar**.

### 3. **Gestión Inteligente de Recursos**
El proyecto utiliza una función personalizada `get_resource_path()` para gestionar rutas. Esto asegura que los iconos y sub-scripts se encuentren correctamente tanto si ejecutas el archivo `.py` como el `.exe` compilado.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
*Developed with ❤️ for music lovers.*
