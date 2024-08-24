FROM python:3.10.5-slim
WORKDIR /app
COPY . . 
RUN python -m pip install -r requirements.txt
CMD python3 bot.py