import vk_api
import os

token = os.environ['TOKEN']

my_token = os.environ['MY_TOKEN']

# Проверка сообщества
def add_new_community_of_link(url):

    group_id = url.split("/")[-1]

    session = vk_api.VkApi(token=token)
    vk = session.get_api()

    try:
        group_info = vk.groups.getById(group_id=group_id, fields='members_count')
        group_members_info = group_info[0]['members_count']

        group_name = group_info[0]['name']
        group_photo = group_info[0]['photo_50']
        # с 1 надо будет поменять на 20к
        if group_members_info >= 1:
            name = group_name
            photo = group_photo
            return {'name': name, 'photo': photo}
        else:
            return False
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False

# мониторинг
def check_user_story_upload(group_id, user_id):
    session = vk_api.VkApi(token=my_token)
    vk = session.get_api()

    try:
        group_info = vk.groups.getById(group_id=group_id, fields="can_upload_story")
        can_upload_story = group_info[0].get("can_upload_story", 0)

        if can_upload_story:
            print(f"Пользователь с ID {user_id} может загружать истории в данную группу.")
        else:
            print(f"Пользователь с ID {user_id} не может загружать истории в данную группу.")

    except vk_api.exceptions.ApiError as e:
        print(f"Произошла ошибка VK API: {e}")

def auto_monitoring(group_id, user_id_to_check):
    check_user_story_upload(group_id, user_id_to_check)

# auto_monitoring("club223942832", "occams.blade")