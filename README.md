# AverisAPI

API avanzada para procesamiento multimedia y voz con funciones mejoradas de video, audio y traducción. Diseñada para proporcionar un conjunto completo de herramientas para manipulación de medios sin costos de suscripción.

## 🚀 Características principales

### Procesamiento de Video
- Composición y manipulación usando FFmpeg
- Subtitulado automático con múltiples estilos
- Concatenación de clips
- Conversión de imágenes a video
- Efectos visuales y filtros avanzados
- Transiciones entre clips
- Mejora de calidad mediante IA

### Procesamiento de Audio
- Conversión a diferentes formatos
- Extracción de audio desde videos
- Mejora de calidad de sonido
- Normalización y ajustes

### Tecnologías de Voz
- Conversión de texto a voz (TTS)
- Traducción de voz entre idiomas
- Transcripción de audio a texto
- Análisis de sentimiento en audio

### Otros
- Ejecución segura de código Python
- Almacenamiento en múltiples proveedores de nube
- API RESTful bien documentada

## 🛠️ Instalación

### Usando Docker

```bash
docker build -t averis-api .
docker run -d -p 8080:8080 \
  -e API_KEY=tu_api_key \
  -e GCP_SA_CREDENTIALS='{"tu":"json_de_cuenta_de_servicio"}' \
  -e GCP_BUCKET_NAME=nombre_de_tu_bucket \
  averis-api
```

### Variables de entorno

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `API_KEY` | Clave para autenticación | Sí |
| `GCP_SA_CREDENTIALS` | Credenciales de Google Cloud | Para almacenamiento GCP |
| `GCP_BUCKET_NAME` | Nombre del bucket GCP | Para almacenamiento GCP |
| `S3_ENDPOINT_URL` | URL del endpoint S3 | Para almacenamiento S3 |
| `S3_ACCESS_KEY` | Clave de acceso S3 | Para almacenamiento S3 |
| `S3_SECRET_KEY` | Clave secreta S3 | Para almacenamiento S3 |

## 📖 Documentación

Consulta la carpeta `/docs` para documentación detallada sobre cada endpoint:
- [Video Processing](/docs/video/)
- [Audio Processing](/docs/audio/)
- [Voice Technologies](/docs/voice/)
- [Storage](/docs/storage/)
- [Code Execution](/docs/code/)

## 🧪 Ejemplos de uso

Próximamente colección de Postman y ejemplos de código en varios lenguajes.

## 👥 Contribuciones

¡Tus contribuciones son bienvenidas! Para aportar al proyecto:
1. Haz un fork del repositorio
2. Crea una rama para tus cambios (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE)

## 🙏 Agradecimientos

Este proyecto está inspirado en [ciberfobia-api](https://github.com/internetesfera/ciberfobia-api) y construido sobre sus conceptos, con mejoras significativas y nuevas funcionalidades.
