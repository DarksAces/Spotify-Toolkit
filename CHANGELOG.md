# Changelog

## [1.0.4] - 2026-03-15

### Fixed
- **UI Responsiveness**: Improved terminal output capture to show interactive prompts (like "Escribe aquí..." or selections) instantly without waiting for a newline.
- **Windows Stability**: Implemented thread-safe UI updates using `.after()` to prevent crashes and "Not Responding" states when running long tasks.
- **Build Process**: Fixed broken directory names in GitHub Actions and `.spec` files (e.g., corrected `Delet Duplicates` to `Delete Duplicates`).
- **Missing Resources**: Added missing `Mood Mixer` and `utils` folders to the compiled executable bundle.
- **Artist Extractor**: Fixed a crash when selecting a playlist due to incorrect return value handling.
- **Shuffle**: Fixed a bug that caused the script to fail silently after choosing a playlist.
- **Playlist Time**: Fixed compatibility with Liked Songs and multi-page playlists.
- **Credentials Marker**: Restored the marker needed for GitHub Secrets injection in the build process.

### Added
- **Bidirectional Communication**: Better support for scripts that require multiple user inputs during execution.
- **Improved Logging**: Logs now scroll automatically and show characters in real-time.


# Historial de Cambios (Changelog)

## [1.0.4] - 2026-03-15

### Corregido
- **Respuesta de la UI**: Se mejoró la captura de salida de la terminal para mostrar mensajes interactivos (como "Escribe aquí..." o selecciones) al instante sin esperar a un salto de línea.
- **Estabilidad en Windows**: Se implementaron actualizaciones de UI seguras para hilos usando `.after()` para evitar bloqueos y estados de "No responde" durante tareas largas.
- **Proceso de Compilación**: Se corrigieron nombres de carpetas erróneos en GitHub Actions y archivos `.spec` (ej: se corrigió `Delet Duplicates` a `Delete Duplicates`).
- **Recursos Faltantes**: Se añadieron las carpetas `Mood Mixer` y `utils` al paquete del ejecutable compilado.
- **Artist Extractor**: Corregido un error al seleccionar una playlist debido al manejo incorrecto del valor de retorno.
- **Shuffle**: Corregido un bug que causaba que el script fallara silenciosamente después de elegir una lista.
- **Playlist Time**: Corregida la compatibilidad con "Canciones Favoritas" y playlists de varias páginas.
- **Marcador de Credenciales**: Se restauró el marcador necesario para la inyección de Secretos de GitHub en el proceso de build.

### Añadido
- **Comunicación Bidireccional**: Mejor soporte para scripts que requieren múltiples entradas del usuario durante su ejecución.
- **Registro (Logging) Mejorado**: Los logs ahora hacen scroll automáticamente y muestran caracteres en tiempo real.
