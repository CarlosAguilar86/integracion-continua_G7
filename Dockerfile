# FROM: La imagen de la que se parte
FROM python:3.12-slim

# WORKDIR: El directorio de trabajo
WORKDIR /app

# COPY: Los archivos de la aplicación que se incluyen
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# EXPOSE: El puerto en el que trabajará el proceso
EXPOSE 8000

# CMD: Lo que se ejecuta al iniciar el contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
