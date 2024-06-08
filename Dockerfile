FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install pyTelegramBotAPI

CMD ["python", "bot.py"]