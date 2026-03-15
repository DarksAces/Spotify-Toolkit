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
