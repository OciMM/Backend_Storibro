import vk_api
import os

token = "vk1.a.BNQK2sS-V-v6zTcG3jkaMukykB5J_xNqfouuzglA5N_MLdJ0I9WYzFw019GdU3UCaucVb8aJX87g5gA4qZQ0cHoFkfPhVdBjXknxvoj6C7JsZbc3SO8_LUvJTut61WBCXrSYgO-dyhwzYik31wdVSl3LAD4dC_x7_hwVVSphU8HcJLTolC9AyKQixAIadphbgoZUeUQDwbsgRUUL9tz9Fg"
my_token = "vk1.a.P8zJ9Yb8YYGO9SkEDMfTKXf9nB7Bv-xUinzEZ3Cdv1Hxqy62I07yXgf84EGtKq4kk4mqbMKFQMROBUOQOuuuK7xFjVlCDmgKcaLuxdE48CQjNHiozcKJv5gp3ZnYE0fh74qlEEaDpqpm5qMQYWVHBH3PmUZNYkeRJ-4B7NtkgDr_-E1CN0hlR2magaO8nylCvEb1WGx6VB5SFX7cAntYGg"

# Проверка сообщества
# по ссылке
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
            count_members = group_members_info
            name = group_name
            photo = group_photo
            return {'name': name, 'photo': photo, 'count_members': count_members}
        else:
            return False
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False

# по названию
def add_new_community_of_name(name):
    session = vk_api.VkApi(token=token)
    vk = session.get_api()

    try:
        group_info = vk.groups.getById(group_id=name, fields='members_count')
        group_members_info = group_info[0]['members_count']

        # group_name = group_info[0]['name']
        group_photo = group_info[0]['photo_50']
        if group_members_info >= 1:
            count_members = group_members_info
            url = "https://vk.com/club" + str(group_info[0]['id'])
            print(url)
            photo = group_photo
            return {'name': name, 'photo': photo, 'count_members': count_members, 'url': url}
        else:
            return False
       
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False
    
# add_new_community_of_name('rexdeus00')

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

# def auto_monitoring(group_id, user_id_to_check):
#     check_user_story_upload(group_id, user_id_to_check)

# auto_monitoring("club223942832", "occams.blade")
        

# функции для поиска доступных сообществ
def list_of_available_communities(user_id):
    session = vk_api.VkApi(token=my_token)
    vk = session.get_api()

    finish_list = []
    finish_list_image = []

    try:
        list_of_groups = vk.groups.get(user_id=user_id, filter="admin", fields="can_upload_story")['items']
        for group in list_of_groups:
            info = vk.groups.getById(group_id=group)
            finish_list.append(info[0]['name'])
            finish_list_image.append(info[0]['photo_50'])
        return finish_list, finish_list_image

    except vk_api.exceptions.ApiError as e:
        print(f"Произошла ошибка VK API: {e}")


def get_int_id(string_id):
    session = vk_api.VkApi(token=my_token)
    vk = session.get_api()

    try:
        info = vk.users.get(user_ids=string_id)
        return info[0]['id']

    except vk_api.exceptions.ApiError as e:
        print(f"Произошла ошибка VK API: {e}")
