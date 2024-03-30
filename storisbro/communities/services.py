import vk_api
import os

token = "vk1.a.MaJjbRLRFk8WS_aZNXRNqQvNQUT7CrAQNv4uKfvjbmtnva_s6Zs4CnSehAEg0vkFYul0qlSa8RnMVE5zWbIvjg_lqfnG8ftvLgwKGyGm21Ncb_X_WEHnAh8YzpabLvSXUVn6Sdb2a1bJDPt5QdeeBjb_PImjjSRiSBPphG4-6OYWGaYX2D1T3WruTVqkZdFmzOqkwL_fjh7qrBankrD_Lw"

my_token = "vk1.a.gIvmwaD-fhiybbPFlByHq7SVYwI4YTp8nd0_ogRz5wiM4PjWF9NAbizaVfXhcj6mWEVIRNEIB62AgR2bCmgW5FOkwwrbRkIeNm0Wlgmq9K2KYuO1cCeY8QtNVYiggtOtzLifu2SMRfLX4iuADp8NjViSoGGR6Dg5TGwYWUzIgFLjXmbqb80zOLnTmwzhvUtv9EqgHPvEECC7qyv1Iqi-4w"

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
