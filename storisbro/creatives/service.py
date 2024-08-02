import vk_api
import requests
from urllib.parse import urlparse
import os

token = "vk1.a.BNQK2sS-V-v6zTcG3jkaMukykB5J_xNqfouuzglA5N_MLdJ0I9WYzFw019GdU3UCaucVb8aJX87g5gA4qZQ0cHoFkfPhVdBjXknxvoj6C7JsZbc3SO8_LUvJTut61WBCXrSYgO-dyhwzYik31wdVSl3LAD4dC_x7_hwVVSphU8HcJLTolC9AyKQixAIadphbgoZUeUQDwbsgRUUL9tz9Fg"
my_token="vk1.a.P8zJ9Yb8YYGO9SkEDMfTKXf9nB7Bv-xUinzEZ3Cdv1Hxqy62I07yXgf84EGtKq4kk4mqbMKFQMROBUOQOuuuK7xFjVlCDmgKcaLuxdE48CQjNHiozcKJv5gp3ZnYE0fh74qlEEaDpqpm5qMQYWVHBH3PmUZNYkeRJ-4B7NtkgDr_-E1CN0hlR2magaO8nylCvEb1WGx6VB5SFX7cAntYGg"

# Проверка ссылки
def check_link_for_story(url, token):
    session = vk_api.VkApi(token=token)
    vk = session.get_api()

    try:
        response = requests.get(url)
        if response.status_code == 200:
            parsed_url = urlparse(url)
            
            if "vk.com" in parsed_url.netloc:
                print(f"Ссылка {url} прошла проверку!")
                return url
            else:
                try:
                    fix_url = vk.utils.getShortLink(url=url)
                    short_link = fix_url['short_url']
                    print(f"Ссылка {url} была из сторонних источников, но мы ее сделали корректной! Вот ссылка - {short_link}")
                    return short_link
                except vk_api.VkApiError as e:
                    print(f"Проверка не получилась, вот ошибка: {e}")
                    return False
        else:
            print(f"Ошибка при проверке ссылки: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Ошибка при проверке ссылки: {e}")
        return False
    
    
# проверка веса файла
# Конвертировать байты в мегабайты
def convert_to_megabytes(size_bytes):
    return size_bytes / (1024 * 1024)

def check_size_file(file):
    if file:
        file_size = file.size
        size_in_mb = convert_to_megabytes(file_size)
        print(f"Размер файла: {size_in_mb:.2f} МБ")

        if 0 < size_in_mb <= 10:
            print("Файл подходит по весу!")
            return True
        else:
            print("Размер слишком большой, нужен файл меньше или возникла другая ошибка.")
            return False
    else:
        return "Файл не найден"
    
# проверка наличия истории
def check_is_story(target_story_id):
    session = vk_api.VkApi(token=my_token)
    vk = session.get_api()

    stories = vk.stories.getById(stories=target_story_id)
    # проверка корректности ссылки
    try:
        if stories['items'][0]['is_deleted']:
            print("История удалена, такое добавить не можем")
            return False
    except KeyError:
        if stories['items'][0]['owner_id'] and stories['items'][0]['id']:
            owner_id_1 = stories['items'][0]['owner_id']
            id_1 = stories['items'][0]['id']
            check_id = str(owner_id_1) + "_" + str(id_1)
            
            if check_id == target_story_id:
                return True
            else:
                return False
        else:
            return False
    

# check_is_story("523037954_456239153")
