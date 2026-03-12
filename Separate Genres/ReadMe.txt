============================================================
🎼 Project - Classify by Genre (English)
============================================================

This Python app allows you to classify the songs of one of your Spotify playlists by genre. The app retrieves genre information from the primary artist of each track and matches it against user-specified genres.

Steps:
1. Authenticate with Spotify
2. Choose a playlist
3. Enter a list of genres
4. The app creates new playlists with tracks matching those genres

Useful for organizing your music based on style.

Requirements:
- Python 3.x
- Spotipy
- A registered Spotify Developer account (for client ID/secret)

============================================================
🎼 Proyecto - Clasificar por Género (Español)
============================================================

Esta aplicación en Python permite clasificar las canciones de una de tus playlists de Spotify por género. La aplicación obtiene la información de género del artista principal de cada canción y la compara con los géneros especificados por el usuario.

Pasos:
1. Autenticarse con Spotify
2. Elegir una playlist
3. Introducir una lista de géneros
4. La aplicación crea nuevas playlists con canciones que coincidan con esos géneros

Útil para organizar tu música por estilo.

Requisitos:
- Python 3.x
- Spotipy
- Una cuenta de desarrollador en Spotify (para ID y secreto)

============================================================
🔑 How to Get Your Spotify Client ID and Secret (English)
============================================================

1. **Create a Spotify Developer Account:**
   - Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Log in with your Spotify account, or create a new one if you don’t have one.

2. **Create an App:**
   - Once logged in, click on **"Create an App"**.
   - Fill out the necessary fields:
     - **App Name:** Choose a name for your app (this can be anything).
     - **App Description:** Add a brief description of your app (e.g., "Playlist Organizer").
     - **Redirect URI:** This is needed for authentication. You can use `http://localhost:8888/callback` or any URL that fits your app (make sure it matches what you use in your code).
   
3. **Get Client ID and Client Secret:**
   - After creating your app, you'll be redirected to the app's dashboard.
   - Here, you'll find your **Client ID** and **Client Secret**. These are the values you’ll need to input in your code.

============================================================
🔑 Cómo Obtener Tu Client ID y Client Secret de Spotify (Español)
============================================================

1. **Crear una Cuenta de Desarrollador de Spotify:**
   - Visita el [Panel de Desarrolladores de Spotify](https://developer.spotify.com/dashboard/applications).
   - Inicia sesión con tu cuenta de Spotify, o crea una nueva si no tienes una.

2. **Crear una Aplicación:**
   - Una vez que hayas iniciado sesión, haz clic en **"Crear una Aplicación"**.
   - Completa los campos necesarios:
     - **Nombre de la Aplicación:** Elige un nombre para tu aplicación (esto puede ser lo que desees).
     - **Descripción de la Aplicación:** Agrega una breve descripción de tu aplicación (por ejemplo, "Organizador de Playlists").
     -
