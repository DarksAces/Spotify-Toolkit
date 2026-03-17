# Changelog

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
