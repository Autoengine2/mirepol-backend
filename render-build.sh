#!/usr/bin/env bash
set -e  # Detiene la ejecución si ocurre algún error

echo "🔄 Actualizando lista de paquetes..."
apt-get update -y

echo "📦 Instalando dependencias del sistema para WeasyPrint..."
apt-get install -y \
  libcairo2 \
  libpango-1.0-0 \
  libgdk-pixbuf2.0-0 \
  libharfbuzz0b \
  libffi-dev \
  libjpeg-dev \
  zlib1g-dev \
  libssl-dev \
  build-essential \
  python3-dev

echo "🐍 Instalando dependencias de Python..."
pip install --upgrade pip
pip install -r requirements.txt

