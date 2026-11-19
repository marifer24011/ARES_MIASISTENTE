
FROM python:3.13-slim

WORKDIR /app

# Instalar dependencias de ARES y del chatbot
COPY backend/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Instalar el modelo de español para ChatterBot
RUN python -m spacy download es_core_news_sm

# Copiar archivos del proyecto
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Copiar el chatbot de Sergio
COPY chatbot_2/ ./chatbot_2/

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
