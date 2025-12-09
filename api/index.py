from http.server import BaseHTTPRequestHandler
import os
import json
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Получаем обновление от Telegram
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        update = json.loads(post_data)

        # 2. Извлекаем сообщение и chat_id
        chat_id = update['message']['chat']['id']
        text = update['message'].get('text', '')

        # 3. Формируем ответ
        if text == '/start':
            reply = "Привет! Я бот без сервера. Просто эхо."
        elif text == '/about':
            reply = "About."
        else:
            reply = f"Вы написали: {text}"

        # 4. Отправляем ответ через API Telegram
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': reply
        }
        requests.post(url, json=payload)

        # 5. Отвечаем Telegram, что обновление обработано
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')