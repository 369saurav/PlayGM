FROM python:3.9.6-bullseye
WORKDIR /app

RUN apt-get install pkg-config
RUN apt-get update && apt-get install -y stockfish

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY core /app/core
COPY routers /app/routers
COPY services /app/services
COPY setup /app/setup

COPY script.sql /app/script.sql
COPY isrgrootx1.pem /app/isrgrootx1.pem

EXPOSE 5000

ENV FLASH_RUN_HOST=0.0.0.0
CMD ["python", "-m", "routers.main_router"]