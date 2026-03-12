# 🎵 Spotify Toolkit

![GitHub release (latest by date)](https://img.shields.io/github/v/release/DarksAces/Spotify-Toolkit?style=for-the-badge&color=1DB954)
![GitHub Repo stars](https://img.shields.io/github/stars/DarksAces/Spotify-Toolkit?style=for-the-badge&color=white)
![GitHub license](https://img.shields.io/github/license/DarksAces/Spotify-Toolkit?style=for-the-badge&color=1DB954)
![Python Version](https://img.shields.io/badge/python-3.9+-yellow?style=for-the-badge&logo=python)

Una colección potente de herramientas con interfaz gráfica para gestionar, limpiar y potenciar tu experiencia en Spotify.
A comprehensive collection of Python scripts to manage, analyze, and optimize your Spotify library. From cleaning duplicates to generating advanced statistics, this toolkit leverages the Spotify API to give you full control over your playlists and liked songs.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Spotify API](https://img.shields.io/badge/API-Spotipy-1DB954.svg)](https://spotipy.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Download & Usage

### For Users (Download EXE)
1. Go to the **Releases** section on the right side of this repository.
2. Download the latest `SpotifyToolkit.exe`.
3. Run it! (No configuration required if built via GitHub Actions).

### For Developers (Run from Source)
1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Spotify-Toolkit.git
   cd Spotify-Toolkit
   ```

2. **Install dependencies:**
   ```bash
   pip install spotipy python-dotenv
   ```

3. **Set up Spotify API Credentials:**
   Create a `.env` file in the root directory with your Spotify Developer credentials:
   ```env
   SPOTIFY_CLIENT_ID='your_client_id'
   SPOTIFY_CLIENT_SECRET='your_client_secret'
   SPOTIFY_REDIRECT_URI='http://localhost:8888/callback'
   ```

## 📖 Usage

Each tool is located in its own directory. You can run them individually:

```bash
# Example: Run the Duplicate Remover
python "Delet Duplicates/delet_duplicates.py"

# Example: Run the Top Tracks analyzer
python "Top Tracks/top_tracks.py"
```

## 🛠️ Automatic Build System (Windows EXE)

This repository is configured with **GitHub Actions** to automatically build a secure, standalone `.exe` file.

1. **Set up Secrets:** In your GitHub repo, go to `Settings > Secrets and variables > Actions` and add:
   - `SPOTIFY_CLIENT_ID`
   - `SPOTIFY_CLIENT_SECRET`
   - `SPOTIFY_REDIRECT_URI` (use `http://127.0.0.1:8888/callback`)
2. **Trigger a build:** Create a new **Release** with a tag like `v1.0.0`.
3. **Result:** The action will compile the code, inject the secrets securely into the binary, and attach the `SpotifyToolkit.exe` to the release.

## 📂 Project Structure

## 🤝 Contributing

Contributions are welcome! If you have a new tool or an improvement, feel free to fork the repo and submit a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Developed with ❤️ for music lovers.*
