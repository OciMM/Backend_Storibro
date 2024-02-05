import vk_api
import os
 
token = os.environ['TOKEN']

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