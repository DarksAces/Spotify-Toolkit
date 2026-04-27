# Changelog

## [1.2.0] - 2026-04-27

### Added
- **🛠️ New Tools Category**: Added a dedicated "Utilities" section in the GUI to better organize the toolkit.
- **🔗 Playlist Merger**: New tool to combine multiple playlists into a new one, with duplicate detection.
- **🎭 Mood Mixer**: Filter any playlist by audio features (Energy, Chill, Danceable, Happy) using Spotify's AI analysis.
- **💾 Library Backup**: One-click full backup of all your playlists and Liked Songs to JSON files.
- **🐛 CLI/GUI Fix**: Resolved a critical bug where sub-scripts would fail to parse arguments when launched from the GUI.

## [1.1.1] - 2026-04-27

### Added
- **📤 Enhanced Metadata Export**: Added CLI arguments support to the export tool. You can now specify playlist IDs and formats via command line.
- **📄 Robust Data Flattening**: Improved CSV export with better flattening of nested Spotify data (Artists, Albums, ISRC, etc.) for better Excel compatibility.
- **🖥️ CLI Menu Expansion**: Integrated Metadata Export and Trend Reports into the CLI menu (`cli_menu.py`).

## [1.1.0] - 2026-04-26

### Added
- **🎵 Full "Liked Songs" Support**: Unified track fetching logic across the entire toolkit. Now you can use your favorite songs in all tools, including Smart Shuffle and Artist Extractor.
- **🛠️ Build System Overhaul**: Updated GitHub Actions and PyInstaller configuration to ensure all dependencies (like `tqdm`) are correctly bundled.
- **🛡️ Credential Robustness**: Improved `.env` loading to handle accidental spaces and quotes.

### Fixed
- **🧹 Bug Fixes**: Resolved merge conflicts in `reorder_tracks.py` and improved progress reporting accuracy.

---

## [1.0.9] - 2026-04-26

### Added
- **🚀 CLI Progress Bars**: Integrated `tqdm` for real-time visual feedback in the terminal for all long-running operations (fetching tracks, processing artists, shuffling, etc.).

### Fixed
- **🧹 Code Cleanup**: Resolved merge conflicts and cleaned up logic in `reorder_tracks.py`.
- **🛠️ Robustness**: Improved progress tracking accuracy across all modules.

---

## [1.0.8] - 2026-04-16

### Added
- **💎 Premium UI Overhaul**: Complete redesign based on the official Spotify dark aesthetic.
- **🗂️ Card-Based Layout**: Tools are now organized in clean, interactive cards for better usability.

---

## [1.0.7] - 2026-04-16

### Added
- **📊 Visual Progress Bar**: Integrated a real-time progress bar in the main GUI to track long-running operations.
- **🎨 Color-coded Logs**: Implemented a system of colored logs for better visual feedback.

---

# Historial de Cambios (Changelog)

## [1.2.0] - 2026-04-27

### Añadido
- **🛠️ Nueva Categoría de Herramientas**: Sección dedicada de "Herramientas" en la interfaz para una mejor organización.
- **🔗 Fusionador de Playlists**: Nueva herramienta para combinar varias listas en una nueva, con detección de duplicados.
- **🎭 Mood Mixer**: Filtra cualquier playlist por características de audio (Energética, Relajada, Bailable, Feliz).
- **💾 Respaldo de Biblioteca**: Copia de seguridad completa de todas tus playlists y canciones favoritas a archivos JSON en un solo clic.
- **🐛 Corrección CLI/GUI**: Solucionado un error crítico donde los sub-scripts fallaban al procesar argumentos al lanzarse desde la interfaz.

## [1.1.1] - 2026-04-27

### Añadido
- **📤 Exportación de Metadatos Mejorada**: Soporte para argumentos de línea de comandos en la herramienta de exportación. Ahora puedes especificar IDs de playlist y formatos vía CLI.
- **📄 Aplanamiento de Datos Robusto**: Mejora en la exportación CSV con un mejor aplanamiento de los datos anidados de Spotify (Artistas, Álbumes, ISRC, etc.) para una mejor compatibilidad con Excel.
- **🖥️ Expansión del Menú CLI**: Integración de la Exportación de Metadatos e Informe de Tendencias en el menú de consola (`cli_menu.py`).

## [1.1.0] - 2026-04-26

### Añadido
- **🎵 Soporte Completo de "Liked Songs"**: Unificada la lógica de obtención de canciones en todo el toolkit. Ahora puedes usar tus canciones favoritas en todas las herramientas, incluyendo Smart Shuffle y Artist Extractor.
- **🛠️ Mejora del Sistema de Build**: Actualizada la GitHub Action y la configuración de PyInstaller para asegurar que todas las librerías (como `tqdm`) se incluyan correctamente.
- **🛡️ Robustez de Credenciales**: Mejora en la carga del archivo `.env` para gestionar espacios y comillas accidentales.

### Corregido
- **🧹 Corrección de Errores**: Resolución de conflictos en `reorder_tracks.py` y mejora en la precisión de las barras de progreso.

---

## [1.0.9] - 2026-04-26

### Añadido
- **🚀 Barras de Progreso en CLI**: Integración de `tqdm` para ofrecer retroalimentación visual en tiempo real en la terminal durante operaciones largas.
