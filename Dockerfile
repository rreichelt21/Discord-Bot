FROM python:3.10.5-slim-bullseye
ENV DiscordToken = ODE1MDA0MTMwNTU2NjQxMzIw.GNt3bL.yVEuKP-lVoIDrw4ikykAENVQCpiVCfawfbiv28

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y ffmpeg

CMD ["python3", "Discord-Bot.py"]