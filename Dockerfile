FROM python:3.10.5-slim-bullseye

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get update && apt-get

CMD ["python3", "Discord-Bot.py"]
