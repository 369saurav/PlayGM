FROM python:3.9

# Install Stockfish
RUN apt-get update && apt-get install -y stockfish
WORKDIR /PlayGM

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "routers/main_router.py"]
