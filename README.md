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
- **Procesamiento por lotes** de múltiples archivos

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

## 📝 Ejemplo de uso

Incluimos un cliente de demostración que muestra cómo utilizar la API:

```bash
# Activar entorno virtual
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Ejecutar demo
python examples/demo_client.py
```

La demo mostrará cómo:
1. Aplicar efectos de video (sepia, dream effect, VHS)
2. Crear videos a partir de imágenes con efecto Ken Burns
3. Convertir texto a voz
4. Ver los idiomas disponibles

También puedes usar programáticamente la API en tus aplicaciones:

```python
import requests

# Configuración
API_KEY = "tu_api_key"
API_URL = "http://localhost:8080"

# Aplicar efecto a un video
def apply_vhs_effect(video_path, output_path):
    url = f"{API_URL}/video/vhs_effect"
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
    data = {
        "video_path": video_path,
        "output_path": output_path,
        "intensity": 0.7
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Ejemplo de uso
result = apply_vhs_effect("input.mp4", "output_vhs.mp4")
print(result)
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

## 📚 API Endpoints

### Video
- `/video/apply_effect` - Aplicar filtros de color básicos
- `/video/add_transition` - Añadir transiciones entre clips
- `/video/enhance` - Mejorar calidad de video
- `/video/apply_overlay` - Añadir overlay/marca de agua
- `/video/timelapse` - Crear timelapse
- `/video/cinematic_bars` - Añadir barras cinematográficas
- `/video/dream_effect` - Aplicar efecto soñador
- `/video/rgb_split` - Efecto RGB split/glitch
- `/video/vhs_effect` - Efecto VHS retro
- `/video/ken_burns` - Efecto Ken Burns para imágenes

### Voz
- `/voice/text_to_speech` - Convertir texto a voz
- `/voice/translate` - Traducir audio entre idiomas
- `/voice/batch_translate` - Procesamiento por lotes
- `/voice/transcribe` - Transcribir audio a texto
- `/voice/languages` - Obtener idiomas disponibles
- `/voice/stream` - Transmitir audio para reproducción

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
