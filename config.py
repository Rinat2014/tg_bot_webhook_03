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
USE_DATABASE = False # bool(SUPABASE_URL and SUPABASE_KEY)

# ===== ADMIN =====
ADMIN_IDS = os.getenv("ADMIN_IDS")  # [123456789]  - array  Замените на ваш chat_id

# ===== LOCAL PATH =====
TEMPLATES_DIR = "templates"
STATUS_HTML = "status.html"

# ===== КОНСТАНТЫ =====
BOT_START_TIME = datetime.now()
VERSION = "0.1.0"