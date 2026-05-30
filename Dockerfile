FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema para PostgreSQL
RUN apt-get update && apt-get install -y \
gcc \
PostgreSQL.client\
&& rm - rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependenciar Python

RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo
COPY . .

# Crear tablas en la base de datos
RUN python -c "fom database import Base, engine; Base.metadata.create_all(bind=engine)" || true
# Comando para iniciar la API
CMD ["uvicorn", "main:app", "--host" "0.0.0.0","--port","8000"]