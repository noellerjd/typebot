FROM python:3.10.5-slim
WORKDIR /app
COPY . . 
RUN python -m pip install -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
CMD python3 bot.py