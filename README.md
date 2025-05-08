# AverisAPI

![CI/CD Pipeline](https://github.com/Nocodeboy/AverisAPI/actions/workflows/ci.yml/badge.svg)

API avanzada para procesamiento multimedia y voz con funciones mejoradas de video, audio y traducción. Diseñada para proporcionar un conjunto completo de herramientas para manipulación de medios sin costos de suscripción.

## 🚀 Características principales

### Procesamiento de Video
- **Composición y manipulación** usando FFmpeg
- **Subtitulado automático** con múltiples estilos
- **Concatenación de clips** con transiciones profesionales
- **Conversión de imágenes a video** con efectos Ken Burns
- **Efectos visuales avanzados**:
  - Filtros de color (grayscale, sepia, vintage, vibrant)
  - Efectos cinematográficos (barras letterbox, dream effect, RGB split)
  - Estilo VHS/retro
  - Overlays y marca de agua
- **Mejora de calidad mediante IA**

### Procesamiento de Audio
- Conversión a diferentes formatos
- Extracción de audio desde videos
- Mejora de calidad de sonido
- Normalización y ajustes

### Tecnologías de Voz
- **Conversión de texto a voz (TTS)** con voces naturales
- **Traducción de voz entre idiomas** con preservación de características vocales
- **Transcripción de audio a texto** usando modelos avanzados
- **Detección automática de idioma**
- **Soporte para más de 15 idiomas**

## 📋 Requisitos

- Python 3.8 o superior
- FFmpeg
- Docker (opcional, para despliegue en contenedor)
- Cuenta de Google Cloud (opcional, para almacenamiento en la nube)

## 🛠️ Instalación rápida

```bash
# Clonar el repositorio
git clone https://github.com/Nocodeboy/AverisAPI.git
cd AverisAPI

# Ejecutar script de configuración
python setup.py
```

El script `setup.py` automatiza:
- Verificación de dependencias del sistema
- Creación del entorno virtual de Python
- Instalación de dependencias
- Configuración de estructura de directorios
- Configuración inicial de variables de entorno

### Instalación manual

```bash
# Clonar el repositorio
git clone https://github.com/Nocodeboy/AverisAPI.git
cd AverisAPI

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores
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

## 🏃‍♂️ Ejecución

```bash
# Activar entorno virtual (si no está activado)
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Iniciar la aplicación
python app.py
```

La API estará disponible en `http://localhost:8080`

### Usando Docker

```bash
# Construir imagen
docker build -t averis-api .

# Ejecutar contenedor
docker run -d -p 8080:8080 \
  -e API_KEY=tu_api_key \
  -e GCP_SA_CREDENTIALS='{"tu":"json_de_cuenta_de_servicio"}' \
  -e GCP_BUCKET_NAME=nombre_de_tu_bucket \
  averis-api
```

## 🧪 Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con cobertura
pytest --cov=core --cov=api
```

## 📖 Documentación

Consulta la carpeta `/docs` para documentación detallada sobre cada endpoint:
- [Video Processing](/docs/video/)
- [Audio Processing](/docs/audio/)
- [Voice Technologies](/docs/voice/)
- [Storage](/docs/storage/)
- [Code Execution](/docs/code/)

## 🚀 En desarrollo (próximas características)

- Interfaz web para demostración
- Más voces y personalización para TTS
- Reconocimiento facial y seguimiento de objetos
- Análisis de sentimiento en audio
- Clonación de voz
- Detección automática de escenas

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
