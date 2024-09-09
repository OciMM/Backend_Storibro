import vk_api
import os
 
token = "Токен пользователя"

def check_link_in_community(community_name, link_to_check):

    community_id_name = community_name.split("/")[-1]
    print(community_id_name)

    session = vk_api.VkApi(token=token)
    vk = session.get_api()

    try:
        group_info = vk.groups.getById(group_id=community_id_name, fields='links')

        if group_info:
            # description = group_info[0]['links'][0]['url']
            des = group_info[0]['links']
            
            lst = []

            link_found = False
            for i in des:
                lst.append(i['url'])
                if link_to_check in lst:
                    print(f"Успешно найдена специальная ссылка в группе")
                    link_found = True

            if link_found == False:
                print("Не получилось найти")
            return link_found
        else:
            print("Не получилось")
            return False
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False

# check_link_in_community("https://vk.com/club223942700", "https://www.shopify.com/blog/low-investment-business-ideas")
    

def check_subscribe(user):
    session = vk_api.VkApi(token=token)
    vk = session.get_api()

    try:
        user_id = vk.users.get(user_ids=user)[0]['id']
        group_id = 'club223942700' # поменять потом на настоящий id сообщества

        result = vk.groups.isMember(group_id=group_id, user_id=user_id)
        
        if result == 1:
            print("Пользователь подписан")
            return True
        
        if result == 0:
            print("Пользователь не подписан")
            return False
    except Exception as e:
        print(f'Ошибка: {e}')


def check_is_comment_board(user_id):
    session = vk_api.VkApi(token=token)
    vk = session.get_api()

    try:
        group_id = 'club223942700' # поменять потом на настоящий id сообщества
        user = vk.users.get(user_ids=user_id)[0]['id']
        group_info = vk.groups.getById(group_id=group_id)[0]['id']
        # user_id = 523037954
        lst = []

        boards_info = vk.board.getTopics(group_id=group_info, extended=1)['profiles']
        for board_info in boards_info:
            lst.append(board_info['id'])

        # print(lst)
        if user in lst:
            print('Он тут есть')
            return True
        else:
            print('Пользователь не найден')
            return False
    except Exception as e:
        print(f"Ошибка: {e}")

# check_is_comment_board(52303954)


# check_subscribe('occams.blade')