# Changelog

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
- **💎 Premium UI Overhaul**: Complete redesign based on the official Spotify dark aesthetic (#121112 / #000000).
- **🗂️ Card-Based Layout**: Tools are now organized in clean, interactive cards for better usability.
- **✨ Iconography Pass**: Refined all menu icons and spacing for pixel-perfect alignment on Windows.

---

## [1.0.7] - 2026-04-16

### Added
- **📊 Visual Progress Bar**: Integrated a real-time progress bar in the main GUI to track long-running operations.
- **🎨 Color-coded Logs**: Implemented a system of colored logs (Success in green, Errors in red, Info in blue) for better visual feedback.
- **📈 Progress Reporting**: Added backend support for reporting progress during track fetching, deletion, and reordering.

### Fixed
- **🛡️ Network Resilience**: Configured auto-retry and timeout strategies for the Spotify client to better handle connectivity issues.
- **⚡ Performance Optimization**: Verified and optimized duplicate detection to maintain O(1) performance for playlists with 5,000+ tracks.

---

## [1.0.6] - 2026-03-17

### Added
- **📦 Metadata Export**: The metadata export tool is now officially included in the compiled distribution.
- **⚡ Automated Builds**: Integrated GitHub Actions with the `Develop` branch for faster tool updates.

### Fixed
- **🛡️ Robustness Improvements**: Prevented crashes when encountering empty playlists or tracks with missing metadata in `utils/helpers.py`.
- **🔄 Pagination Logic**: Improved API pagination and added safety checks for large libraries.

---

## [1.0.5] - 2026-03-16

### Added
- **🌍 Internationalization (i18n)**: Added automatic English/Spanish detection based on OS locale for both the UI and console output.
- **📝 Contextual Help**: Added descriptions for every tool within the GUI to improve user guidance.
- **🔍 Smart Search**: Enhanced the playlist selection screen to allow searching by name instead of just numbers.
- **🛠️ Documentation**: Added `requirements.txt` and `.env.example` for easier development setup.

### Fixed
- **📁 Standardized Structure**: Renamed all folders and scripts to follow standardized naming conventions (snake_case) for better command-line compatibility.
- **🚀 Main Entry Point**: Unified the main application file as `main.py`.
- **🐛 Bug Fixes**: Fixed several naming inconsistencies (e.g., `delet_duplicates` to `delete_duplicates`).
- **📦 Build System**: Updated `.spec` files to reflect the new standardized folder structure.

---

## [1.0.4] - 2026-03-15

### Fixed
- **UI Responsiveness**: Improved terminal output capture to show interactive prompts instantly.
- **Windows Stability**: Implemented thread-safe UI updates using `.after()`.
- **Build Process**: Fixed broken directory names in GitHub Actions and `.spec` files.

---

# Historial de Cambios (Changelog)

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
- **🚀 Barras de Progreso en CLI**: Integración de `tqdm` para ofrecer retroalimentación visual en tiempo real en la terminal durante operaciones largas (descarga de canciones, análisis de artistas, mezclas, etc.).

### Corregido
- **🧹 Limpieza de Código**: Resolución de conflictos de fusión y limpieza de lógica en `reorder_tracks.py`.
- **🛠️ Robustez**: Mejora en la precisión del seguimiento de progreso en todos los módulos.

---

## [1.0.8] - 2026-04-16

### Añadido
- **💎 Rediseño Premium**: Rediseño completo de la interfaz basado en la estética oscura oficial de Spotify.
- **🗂️ Diseño por Tarjetas**: Las herramientas ahora están organizadas en tarjetas interactivas más limpias y fáciles de usar.
- **✨ Refinado de Iconos**: Ajuste de pixel-perfect en todos los iconos y espaciados del menú lateral.

---

## [1.0.7] - 2026-04-16

### Añadido
- **📊 Barra de Progreso Visual**: Integración de una barra de progreso en tiempo real en la interfaz principal para tareas largas.
- **🎨 Logs con Colores**: Implementación de un sistema de colores en el registro (Éxito en verde, Errores en rojo, Info en azul) para una mejor respuesta visual.
- **📈 Reporte de Avance**: Añadido soporte en los scripts para informar del progreso durante la descarga, borrado y reordenación de canciones.

### Corregido
- **🛡️ Resiliencia de Red**: Configuración de estrategias de reintento automático y tiempos de espera para gestionar mejor los cortes de conexión.
- **⚡ Optimización de Rendimiento**: Verificación y optimización de la detección de duplicados para mantener rendimiento O(1) en listas de más de 5.000 canciones.

---

## [1.0.6] - 2026-03-17

### Añadido
- **📦 Exportación de Metadatos**: La herramienta para exportar metadatos ya está incluida oficialmente en la versión compilada.
- **⚡ Builds Automatizados**: Integración de GitHub Actions con la rama `Develop` para actualizaciones más rápidas.

### Corregido
- **🛡️ Mejoras de Robustez**: Se evitaron cierres inesperados al encontrar playlists vacías o canciones con metadatos incompletos en `utils/helpers.py`.
- **🔄 Lógica de Paginación**: Se mejoró la paginación de la API y se añadieron comprobaciones de seguridad para bibliotecas grandes.

---

## [1.0.5] - 2026-03-16

### Añadido
- **🌍 Internacionalización (i18n)**: Detección automática de Inglés/Español basada en el sistema tanto para la interfaz como para la salida de consola.
- **📝 Ayuda Contextual**: Se añadieron descripciones para cada herramienta en la interfaz para guiar mejor al usuario.
- **🔍 Búsqueda Inteligente**: Se mejoró la selección de playlists permitiendo buscar por nombre además de por número.
- **🛠️ Documentación**: Se añadieron los archivos `requirements.txt` y `.env.example` para facilitar la configuración a desarrolladores.

### Corregido
- **📁 Estructura Normalizada**: Se renombraron todas las carpetas y scripts siguiendo convenciones estándar (snake_case) para una mayor compatibilidad.
- **🚀 Punto de Entrada Principal**: Se unificó el archivo principal como `main.py`.
- **🐛 Corrección de Errores**: Corregidas varias inconsistencias de nombres (ej: de `delet_duplicates` a `delete_duplicates`).
- **📦 Sistema de Compilación**: Actualizados los archivos `.spec` para reflejar la nueva estructura de carpetas.

---

## [1.0.4] - 2026-03-15
... (resto del historial)
