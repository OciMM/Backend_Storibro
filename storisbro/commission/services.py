import vk_api
import os

token = os.environ['TOKEN']

def check_link_in_community(community_name, link_to_check):

    session = vk_api.VkApi(token=token)
    vk = session.get_api()

    try:
        group_info = vk.groups.getById(group_id=community_name, fields='links')

        if group_info:
            # description = group_info[0]['links'][0]['url']
            des = group_info[0]['links']
            
            lst = []

            link_found = False
            for i in des:
                lst.append(i['url'])
                if link_to_check in lst:
                    link_found = True

            return link_found
        else:
            return False
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False
