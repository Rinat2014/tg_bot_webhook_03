"""
Модуль для работы с базой данных Supabase
"""

import os
from datetime import datetime
from config import USE_DATABASE, SUPABASE_URL, SUPABASE_KEY

if USE_DATABASE:
    try:
        import supabase
        supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
    except ImportError:
        print("Библиотека supabase не установлена")
        supabase_client = None
        USE_DATABASE = False
else:
    supabase_client = None

def save_user(chat_id, user_data):
    """Сохраняет или обновляет пользователя"""
    if not USE_DATABASE or not supabase_client:
        return None
    
    try:
        user_info = {
            'chat_id': chat_id,
            'username': user_data.get('username'),
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
            'last_activity': datetime.now().isoformat()
        }
        
        # Проверяем существование
        response = supabase_client.table('users') \
            .select('*') \
            .eq('chat_id', chat_id) \
            .execute()
        
        if len(response.data) == 0:
            # Новый пользователь
            result = supabase_client.table('users').insert(user_info).execute()
            print(f"Создан пользователь {chat_id}")
            return result
        else:
            # Обновляем
            result = supabase_client.table('users') \
                .update(user_info) \
                .eq('chat_id', chat_id) \
                .execute()
            print(f"Обновлен пользователь {chat_id}")
            return result
            
    except Exception as e:
        print(f"Ошибка сохранения пользователя: {e}")
        return None

def get_user_stats(chat_id):
    """Получает статистику пользователя"""
    if not USE_DATABASE or not supabase_client:
        return None
    
    try:
        response = supabase_client.table('users') \
            .select('*') \
            .eq('chat_id', chat_id) \
            .execute()
        
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Ошибка получения статистики: {e}")
        return None

def get_all_users(limit=50):
    """Получает список всех пользователей"""
    if not USE_DATABASE or not supabase_client:
        return []
    
    try:
        response = supabase_client.table('users') \
            .select('*') \
            .order('created_at', desc=True) \
            .limit(limit) \
            .execute()
        return response.data
    except Exception as e:
        print(f"Ошибка получения пользователей: {e}")
        return []