FROM python:3.10-slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

RUN apt-get update && apt-get install -y ffmpeg

CMD ["python3", "Discord-Bot.py"]