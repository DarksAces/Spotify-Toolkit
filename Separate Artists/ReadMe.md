============================================================
🎵 Project - Classify by Artist or Similar Artists (English)
============================================================

This Python app connects to your Spotify account, retrieves your playlists, and allows you to select one. It then analyzes the tracks in that playlist and gives you the option to classify them either:

- By the original artist of each track
- By similar artists, using Spotify's related artist data

Once classified, it creates new playlists grouping the tracks accordingly.

Requirements:
- Python 3.x
- Spotipy
- A registered Spotify Developer account (for client ID/secret)

============================================================
🎵 Proyecto - Clasificar por Artista o Artistas Similares (Español)
============================================================

Esta aplicación en Python se conecta a tu cuenta de Spotify, obtiene tus playlists y te permite seleccionar una. Luego analiza las canciones de esa playlist y te da la opción de clasificarlas:

- Por el artista original de cada canción
- Por artistas similares, usando los datos de artistas relacionados de Spotify

Una vez clasificadas, la app crea nuevas playlists agrupando las canciones según tu elección.

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
     - **Redirect URI:** Esto es necesario para la autenticación. Puedes usar `http://localhost:8888/callback` o cualquier URL que se ajuste a tu aplicación (asegúrate de que coincida con la que usas en tu código).

3. **Obtener el Client ID y Client Secret:**
   - Después de crear tu aplicación, serás redirigido al panel de la aplicación.
   - Aquí encontrarás tu **Client ID** y **Client Secret**. Estos son los valores que necesitarás ingresar en tu código.
