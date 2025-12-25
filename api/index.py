"""
Основной обработчик для Vercel Serverless Function
"""

import os
import sys
import json
import requests
from datetime import datetime
from http.server import BaseHTTPRequestHandler

# Добавляем родительскую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import *
from db_manager import save_user, get_user_stats

# Импортируем базу данных если настроена
if USE_DATABASE:
    from db_manager import supabase_client
else:
    supabase_client = None

def read_html_template():
    """Читает HTML шаблон из файла"""
    try:
        template_path = os.path.join(TEMPLATES_DIR, STATUS_HTML)
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # Fallback минимальный HTML
        return """
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>Bot started</title>
        <style>
            body {margin:0;padding:0;display:flex;justify-content:center;align-items:center;min-height:100vh;background:#f5f5f5;}
            .box {border:3px solid #4CAF50;padding:40px;background:white;border-radius:10px;text-align:center;}
        </style>
        </head>
        <body><div class="box"><h2>🤖 Bot started</h2></div></body>
        </html>
        """

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Обработка GET-запросов - показываем статусную страницу"""
        html_content = html_status__bot_started # read_html_template()
        
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def do_POST(self):
        """Обработка POST-запросов от Telegram Webhook"""
        print(f"Get webhook", datetime.now().isoformat() )
        try:
            # 1. Получаем данные от Telegram
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update = json.loads(post_data)
            
            # 2. Извлекаем сообщение
            message = update.get('message', {})
            if not message:
                self.send_response(200)
                self.end_headers()
                return
            
            chat = message.get('chat', {})
            chat_id = chat.get('id')
            text = message.get('text', '').strip()
            user = message.get('from', {})
            
            # 3. Сохраняем пользователя (если есть база)
            if USE_DATABASE:
                save_user(chat_id, user)
            
            # 4. Обрабатываем команды
            reply = self.process_command(text, chat_id, user)
            
            # 5. Отправляем ответ
            self.send_telegram_message(chat_id, reply)
            
            # 6. Отвечаем Telegram
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
            
        except Exception as e:
            print(f"Ошибка: {e}")
            self.send_response(500)
            self.end_headers()
    
    def process_command(self, text, chat_id, user):
        """Обрабатывает текстовые команды"""
        commands = {
            '/start': f"Привет, {user.get('first_name', 'друг')}! Я бот на Vercel. \nКоманды: /help",
            '/help': "Доступные команды:\n/start - Приветствие\n/help - Помощь\n/about - О боте\n/stats - Статистика",
            '/about': f"Бот: {PROJECT_NAME}\nВерсия: {VERSION}\nХостинг: Vercel",
            '/stats': self.get_stats_for_user(chat_id) if USE_DATABASE else "База данных не настроена",
        }
        
        # Проверяем точное совпадение команд
        if text in commands:
            return commands[text]
        
        # Для админов дополнительные команды
        if str(chat_id) in ADMIN_IDS and text == '/admin':
            return "Панель администратора\n/users - список пользователей"
            
        # Любой другой текст
        return f"Вы написали: {text}\nИспользуйте \n/help для списка команд"
    
    def get_stats_for_user(self, chat_id):
        """Получает статистику пользователя"""
        try:
            if not USE_DATABASE:
                return "Статистика недоступна"
            
            stats = get_user_stats(chat_id)
            if stats:
                return f"""Ваша статистика:
👤: {stats.get('first_name', '')}
📅: {stats.get('created_at', '')[:10]}
💬: {stats.get('message_count', 0)} сообщений"""
            return "Статистика не найдена"
        except Exception as e:
            print(f"Ошибка получения статистики: {e}")
            return "Ошибка получения статистики"
    
    def send_telegram_message(self, chat_id, text):
        """Отправляет сообщение в Telegram"""
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Ошибка отправки в Telegram: {e}")





def main():
    pass

if __name__ == "__main__":
    main()