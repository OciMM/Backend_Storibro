# из файла TG.py
import os
from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import MessageHandler, filters

TOKEN = ''
CHANNEL_USERNAME = ''

def get_latest_video(update: Update, context: CallbackContext) -> None:
    try:
        user_channel = context.args[0] if context.args else CHANNEL_USERNAME

        bot = context.bot

        # Получаем последнее сообщение
        messages = bot.get_chat_history(chat_id=user_channel, limit=1)
        latest_message = messages[0]

        # Проверяем, является ли последнее сообщение видео
        if latest_message.media_group and latest_message.media_group[0].document.mime_type == 'video/mp4':
            video_file = latest_message.media_group[0].document.file_id

            # Получаем видео N+155
            n_plus_155_index = min(len(messages), 155)  # Обеспечиваем, чтобы не выйти за границы
            video_n_plus_155 = messages[n_plus_155_index - 1].media_group[0].document.file_id

            # Выполняем необходимые действия с video_file и video_n_plus_155 
            # ...

        else:
            # Обрабатываем случай, когда последнее сообщение не является видео
            update.message.reply_text("Последнее сообщение не является видео.")

    except Exception as e:
        # Обрабатываем исключения
        update.message.reply_text(f"Произошла ошибка: {str(e)}")

def main() -> None:
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("get_latest_video", get_latest_video, pass_args=True))

    updater.start_polling()
    updater.idle()

# if __name__ == '__main__':
#     main()


# из файла bot.py
import requests
import vk_api
from vk_api.utils import get_random_id
from moviepy.editor import VideoFileClip
import io

v = '5.199'
group_id = ''  
access_token = ''  
upload_url = None
upload_result = None
link_text = [
    'to_store', 
    'vote more', 
    'book', 
    'order', 
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


# if __name__ == '__main__':
#     first()
#     second()
#     third()


# из файла stats.py
    
import re

def extract_owner_post_ids(url):
    match = re.search(r'wall-(\d+)_(\d+)', url)
    if match:
        owner_id = int(match.group(1))
        post_id = int(match.group(2))
        return owner_id, post_id
    else:
        print("Неверный формат ссылки")

# Пример использования
url = 'vk.com/wall-29246653_184828'
owner_id, post_id = extract_owner_post_ids(url)


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

access_token = 'Ваш_токен'

# story_stats = get_story_stats(owner_id, story_id, access_token)
# if story_stats:
#     print("Статистика истории:", story_stats)