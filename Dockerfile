FROM python:3.10-slim

# Устанавливаем прокси-сервер (Xray-core)
RUN apt-get update && apt-get install -y curl unzip && \
    curl -L https://github.com/XTLS/Xray-core/releases/download/v1.8.6/Xray-linux-64.zip -o xray.zip && \
    unzip xray.zip -d /usr/local/bin/ && \
    rm xray.zip && \
    chmod +x /usr/local/bin/xray

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запускаем прокси и бота
CMD /usr/local/bin/xray -config /app/config.json & python bot.py
