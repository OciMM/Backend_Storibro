import requests
import vk_api
from vk_api.utils import get_random_id
from moviepy.editor import VideoFileClip
import io


# Создаем таблицу в базе данных, если ее не существует

import os
import sqlite3
from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import MessageHandler

TOKEN = '7012789226:AAEXiuLkNLPj9r7Yv4suBLmbtc4rZ08WBbI'
CHANNEL_USERNAME = 'Storisbro_test_bot'
DATABASE_FILE = 'video_tracker.sqlite3'


# Создаем таблицу в базе данных, если ее не существует
def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            channel TEXT,
            file_id TEXT,
            PRIMARY KEY (channel, file_id)
        )
    ''')
    conn.commit()
    conn.close()

# было ли видео уже обработано
def is_video_processed(channel, file_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM videos WHERE channel=? AND file_id=?', (channel, file_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Функция для отметки видео как обработанного
def mark_video_processed(channel, file_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO videos (channel, file_id) VALUES (?, ?)', (channel, file_id))
    conn.commit()
    conn.close()


def get_latest_video(update: Update, context: CallbackContext) -> None:
    try:
        user_channel = context.args[0] if context.args else CHANNEL_USERNAME
        bot = context.bot

        messages = bot.get_chat_history(chat_id=user_channel, limit=1)
        
        # Добавим вывод для отладки
        print("Received messages:", messages)
        
        if messages:
            latest_message = messages[0]

            if (
                latest_message.media_group
                and latest_message.media_group[0].document.mime_type == 'video/mp4'
                and not is_video_processed(user_channel, latest_message.media_group[0].document.file_id)
            ):
                video_file = latest_message.media_group[0].document.file_id

                # Обрабатываем видео
                
                # Отмечаем видео как обработанное
                mark_video_processed(user_channel, video_file)
                print(f"Video marked as processed: {user_channel}, {video_file}")

            else:
                # Обрабатываем случай, когда последнее сообщение не является новым видео
                update.message.reply_text("Последнее сообщение не является новым видео или уже было обработано.")
        else:
            # Обрабатываем случай, когда не удалось получить сообщения из чата
            update.message.reply_text("Не удалось получить последнее сообщение из чата.")

    except Exception as e:
        # Обрабатываем исключения
        update.message.reply_text(f"Произошла ошибка: {str(e)}")

def main() -> None:
    # Создаем таблицу в базе данных
    create_table()

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("get_latest_video", get_latest_video, pass_args=True))
    print("Вроде бы работает")

    updater.start_polling()
    updater.idle()
    print('Точно работает')

if __name__ == '__main__':
    main()

# из файла bot.py
v = '5.199'
group_id = ''  
access_token = ''  
upload_url = None
upload_result = None
link_text = [
'to_store', 
'vote more', 
'book', 'order', 
'enrol', 
'fill', 
'signup', 
'buy', 
'ticket', 
'write', 
'open', 
'learn_more', 
'view', 
'go_to', 
'contact', 
'watch', 
'play', 
'install', 
'read' 
]
#
#to_store — В магазин.
#vote — Голосовать.
#more — Ещё.
#book — Забронировать.
#order — Заказать.
#enroll — Записаться.
#fill — Заполнить.
#signup — Зарегистрироваться.
#buy — Купить.
#ticket — Купить билет.
#write — Написать.
#open — Открыть.
#learn_more — Подробнее. Значение используется по умолчанию.
#view — Посмотреть.
#go_to — Перейти.
#contact — Связаться.
#watch — Смотреть.
#play — Слушать.
#install — Установить.
#read — Читать.
def first():
    global upload_url  
    url = 'https://api.vk.com/method/stories.getVideoUploadServer'


    params = {
        'v': v,
        'access_token': access_token,
        'add_to_news': 1,
        'group_id': group_id,
        'link_text' : link_text
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        upload_url = data['response']['upload_url']
        return upload_url

def second():
    global upload_result  

    files = {
        'file': ('video.mp4', open('', 'rb'))  #нужно сделать, чтобы грузило загруженный видос
    }
    video_clip = VideoFileClip(io.BytesIO(files))
    duration = video_clip.duration
    aspect_ratio = video_clip.size[0] / video_clip.size[1]
    video_clip.close()

    if duration > 15 or aspect_ratio != 9 / 16:
        print('Неверная длительность или соотношение сторон видео. Загрузка отменена.')
        return
    response = requests.post(upload_url, files=files)

    if response.status_code == 200:
        data = response.json()
        upload_result = data['response'].get('upload_result')
        return upload_result

def third():
    url = 'https://api.vk.com/method/stories.save'

    params = {
        'access_token': access_token,
        'upload_results': upload_result,
        'v': v,
    }

    response = requests.post(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(data)


#из файла stats.py
import re
import vk_api

def extract_owner_post_ids(url):
    match = re.search(r'wall-(\d+)_(\d+)', url)
    if match:
        owner_id = int(match.group(1))
        post_id = int(match.group(2))
        return owner_id, post_id
    else:
        print("Неверный формат ссылки")

# Пример использования
# url = 'vk.com/wall-523037954_456239154'
# owner_id, post_id = extract_owner_post_ids(url)

# print(owner_id, post_id)

import requests

def get_story_stats(owner_id, story_id, access_token):
    api_url = "https://api.vk.com/method/stories.getStats"
    
    params = {
        'owner_id': owner_id,
        'story_id': story_id,
        'access_token': access_token,
        'v': '5.131'  
    }

    response = requests.get(api_url, params=params)
    data = response.json()

    if 'error' in data:
        print(f"Ошибка: {data['error']['error_msg']}")
        return None
    else:
        return data['response']

# Пример использования

# access_token = 'vk1.a.VRPvF6Ouca-cD1KJMALPpD2n244LYOWc0zL4cfDYFCkY1CciuAGWRvz6Rt9PAyIUHMunZLONl8H9y-3pmdxYy64xmjBYzqZ7QxrwuIUx5mBVp0Mc2qym0VWJ0loxf1f7lVX9EOIrwMU5WfLbawdPfzwE3XgrZBpwWo5KDn3zuxfx7IUM6HPgs4KwvtACbSAdwzKxkHwodWIPzt0c6V52dA'

# story_stats = get_story_stats(owner_id, post_id, access_token)
# if story_stats:
#     print("Статистика истории:", story_stats)