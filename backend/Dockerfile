FROM python:3.11-slim

# Crear carpeta de trabajo
WORKDIR /app

# Instalar dependencias del sistema para openpyxl, etc
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalarlos
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Crear carpetas necesarias
RUN mkdir -p uploads data

EXPOSE 3001

CMD ["python", "app.py"]
