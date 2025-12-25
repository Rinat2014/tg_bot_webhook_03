# telegram-bot/
# │
# ├── api/
# │   └── index.py              # Основной обработчик для Vercel (обязательно!)
# │
# ├── templates/
# │   └── status.html           # HTML шаблон для статусной страницы
# │
# ├── config.py                 # Конфигурация и настройки
# ├── db_manager.py             # Работа с базой данных Supabase
# ├── bot_handlers.py           # Логика обработки команд бота (опционально)
# ├── requirements.txt          # Зависимости Python
# ├── vercel.json               # Конфигурация Vercel (опционально)
# └── .gitignore                # Игнорируемые файлы


"""
Конфигурация Telegram бота
"""

import os
from datetime import datetime

# ===== TOKEN  =====
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ===== DATABASE =====
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
USE_DATABASE = bool(SUPABASE_URL and SUPABASE_KEY)

# ===== ADMIN =====
ADMIN_IDS = os.getenv("ADMIN_IDS")  # [123456789]  - array  Замените на ваш chat_id

# ===== LOCAL PATH =====
TEMPLATES_DIR = "templates"
STATUS_HTML = "status.html"

# ===== КОНСТАНТЫ =====
BOT_START_TIME = datetime.now()
PROJECT_NAME = "tg_bot_webhook_03"
VERSION = "0.1.0"




# ===== КОНСТАНТЫ =====
html_status__bot_started = """
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