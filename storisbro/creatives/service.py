import vk_api
import requests
from urllib.parse import urlparse
import os

token = "vk1.a.ajlwaqRZeEgOfznuUVqmjJI4D2-luGPdCJlwT1JxTPDxn2pvfjTdvG84PrsM_J30mQqWK5VXKPxHpnr7c2PqzgbPCd_aeyVI-gAmUBVoX_1qi6Vet3hH-CXwWV4axHpgJgKmD87N9vqBY37h-LRX2j8qOl4ctQ4Fm4M7XYF3VOIW18wdMFdz-qdZgo61v7rJ5nH3I6hchHWNQTlFcKD5IQ"

my_token = "vk1.a.gIvmwaD-fhiybbPFlByHq7SVYwI4YTp8nd0_ogRz5wiM4PjWF9NAbizaVfXhcj6mWEVIRNEIB62AgR2bCmgW5FOkwwrbRkIeNm0Wlgmq9K2KYuO1cCeY8QtNVYiggtOtzLifu2SMRfLX4iuADp8NjViSoGGR6Dg5TGwYWUzIgFLjXmbqb80zOLnTmwzhvUtv9EqgHPvEECC7qyv1Iqi-4w"

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
        