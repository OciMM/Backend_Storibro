import vk_api
import requests

import os

token = "vk1.a.MaJjbRLRFk8WS_aZNXRNqQvNQUT7CrAQNv4uKfvjbmtnva_s6Zs4CnSehAEg0vkFYul0qlSa8RnMVE5zWbIvjg_lqfnG8ftvLgwKGyGm21Ncb_X_WEHnAh8YzpabLvSXUVn6Sdb2a1bJDPt5QdeeBjb_PImjjSRiSBPphG4-6OYWGaYX2D1T3WruTVqkZdFmzOqkwL_fjh7qrBankrD_Lw"

my_token = "vk1.a.gIvmwaD-fhiybbPFlByHq7SVYwI4YTp8nd0_ogRz5wiM4PjWF9NAbizaVfXhcj6mWEVIRNEIB62AgR2bCmgW5FOkwwrbRkIeNm0Wlgmq9K2KYuO1cCeY8QtNVYiggtOtzLifu2SMRfLX4iuADp8NjViSoGGR6Dg5TGwYWUzIgFLjXmbqb80zOLnTmwzhvUtv9EqgHPvEECC7qyv1Iqi-4w"

# Проверка ссылки
def check_link_for_story(url):
    session = vk_api.VkApi(token=token)
    vk = session.get_api()

    try:
        response = requests.get(url)
        if response.status_code == 200:

            try:
                correct_url = url.split(".")[0]
                
                if correct_url == "https://vk":
                    print(f"Ссылка {url} прошла проверку!")
                    return url
                
                elif correct_url != "https://vk":
                    fix_url = vk.utils.getShortLink(url=url)
                    short_link = fix_url['short_url']
                    print(f"Ссылка {url} была из сторонних источников, но мы ее сделали корректной! Вот ссылка - {short_link}")
                    return short_link
                
                else:
                    print("Что-то пошло не так :(")
                    return False
            except vk_api.VkApiError as e:
                print(f"Проверка не получилась, вот ошибка: {e}")
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
        