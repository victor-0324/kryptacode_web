FROM python:3.11-slim

# define /app como raiz do seu container
WORKDIR /app

# copia apenas requirements e instala (incluindo gunicorn)
COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

RUN mkdir -p /app/src/database
COPY src/ .

# expõe a porta do seu Flask/Gunicorn
EXPOSE 5000

# inicia o Gunicorn apontando para src.wsgi:app
CMD ["gunicorn", "wsgi:app", "--bind=0.0.0.0:5000", "--workers=1", "--timeout=180"]
