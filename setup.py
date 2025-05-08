#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Verifica si las dependencias del sistema están instaladas"""
    print("🔍 Verificando dependencias del sistema...")
    
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("✅ FFmpeg está instalado")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ FFmpeg no está instalado. Por favor instálalo para continuar.")
        print("   Ubuntu/Debian: sudo apt install ffmpeg")
        print("   macOS: brew install ffmpeg")
        print("   Windows: Descarga desde https://ffmpeg.org/download.html")
        sys.exit(1)
    
    print("✅ Todas las dependencias del sistema están instaladas")

def setup_virtual_environment():
    """Configura el entorno virtual de Python"""
    print("\n🐍 Configurando entorno virtual de Python...")
    
    if os.path.exists("venv"):
        print("🔄 Entorno virtual existente, actualizando...")
    else:
        print("🆕 Creando nuevo entorno virtual...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    # Determinar script de activación según plataforma
    if sys.platform == "win32":
        python_exe = os.path.join("venv", "Scripts", "python.exe")
    else:
        python_exe = os.path.join("venv", "bin", "python")
    
    # Instalar/actualizar dependencias
    print("📦 Instalando dependencias...")
    subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([python_exe, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    print("✅ Entorno virtual configurado correctamente")

def setup_project_structure():
    """Crea directorios necesarios para el proyecto"""
    print("\n📁 Configurando estructura del proyecto...")
    
    # Directorios para archivos temporales
    for directory in ["temp", "temp/uploads", "temp/output", "temp/cache"]:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directorio {directory} verificado")
    
    # Directorio para muestras
    for directory in ["samples", "samples/video", "samples/audio", "samples/images"]:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directorio {directory} verificado")
    
    print("✅ Estructura de directorios configurada correctamente")

def setup_env_file():
    """Configura el archivo .env si no existe"""
    print("\n🔧 Configurando variables de entorno...")
    
    if not os.path.exists(".env"):
        shutil.copy(".env.example", ".env")
        print("✅ Archivo .env creado desde .env.example")
        print("   ⚠️ IMPORTANTE: Edita el archivo .env con tus credenciales")
    else:
        print("✅ Archivo .env ya existe")

def download_sample_files():
    """Descarga algunos archivos de muestra para pruebas"""
    print("\n📥 Descargando archivos de muestra...")
    
    # Esta función podría implementarse usando urllib o requests
    # para descargar archivos de prueba de algún repositorio o CDN
    
    print("⏳ Esta funcionalidad será implementada próximamente")
    print("   Por ahora, puedes añadir tus propios archivos a la carpeta 'samples/'")

def main():
    """Función principal"""
    print("🚀 Iniciando configuración de AverisAPI...")
    
    check_dependencies()
    setup_virtual_environment()
    setup_project_structure()
    setup_env_file()
    download_sample_files()
    
    print("\n✨ ¡Configuración completada con éxito! ✨")
    print("\nPara iniciar el desarrollo:")
    if sys.platform == "win32":
        print("   1. Activa el entorno virtual: .\\venv\\Scripts\\activate")
    else:
        print("   1. Activa el entorno virtual: source venv/bin/activate")
    print("   2. Inicia la aplicación: python app.py")
    print("   3. Accede a la API en: http://localhost:8080")
    print("\n📚 Consulta la documentación en la carpeta 'docs/' para más información")

if __name__ == "__main__":
    main()
