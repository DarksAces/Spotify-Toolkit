# Changelog

## [1.1.1] - 2026-04-27

### Added
- **🎨 UI Redesign**: New card-based grid layout, active navigation indicators, and dark mode adjustments.
- **🛠️ New Tools**: Playlist Merger, Mood Mixer, and Library Backup.
- **📤 Enhanced Metadata Export**: Added CLI arguments and data flattening for CSV/JSON.
- **📁 Centralized Exports**: Files are now saved in a dedicated `exports/` folder.
- **🌍 Dynamic i18n**: Language toggle (EN/ES) in the sidebar.
- **🐛 CLI/GUI Fix**: Resolved bug in sub-script argument parsing.

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

## [1.1.1] - 2026-04-27

### Añadido
- **🎨 Rediseño de Interfaz**: Nuevo diseño de tarjetas en cuadrícula, indicadores de navegación y ajustes de tema oscuro.
- **🛠️ Nuevas Herramientas**: Fusionador de Playlists, Mood Mixer y Respaldo de Biblioteca.
- **📤 Exportación Mejorada**: Soporte CLI y aplanamiento de datos para CSV/JSON.
- **📁 Exportaciones Centralizadas**: Carpeta `exports/` dedicada para los archivos generados.
- **🌍 i18n Dinámico**: Cambio de idioma (EN/ES) en la barra lateral.
- **🐛 Corrección CLI/GUI**: Solucionado error de argumentos en scripts secundarios.

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
