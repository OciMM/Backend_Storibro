from celery import shared_task
from commission.services import check_link_in_community, check_subscribe, check_is_comment_board
from communities.models import CommunityModel

# функция которая активируется автоматически в случайное время (настройки celery.py)
@shared_task(bind=True)
def run_patch_task(self):
    # Ваш код для вызова метода patch здесь
    # Например:

    public_models = CommunityModel.objects.all()
    for public_model in public_models:
        link_found = check_link_in_community(public_model.url, public_model.url_commission)
        subscription_status = check_subscribe(public_model.user.vk_id)
        is_comment_board = check_is_comment_board(public_model.user.vk_id)
        print(f"Link found for {public_model.name}: {link_found}")

        if link_found and subscription_status and is_comment_board:
            public_model.status_commission = True
        else:
            public_model.status_commission = False
        public_model.save()

    public_model.refresh_from_db()


# функция которая активируется при нажатие кнопки
@shared_task(bind=True)
def run_patch_task_button(self, user_id):
    try:
        public_models = CommunityModel.objects.filter(user=user_id)
        for public_model in public_models:
            link_found = check_link_in_community(public_model.url, public_model.url_commission)
            subscription_status = check_subscribe(public_model.user.vk_id)
            is_comment_board = check_is_comment_board(public_model.user.vk_id)
            print(f"Link found for {public_model.name}: {link_found}")

            if link_found and subscription_status and is_comment_board:
                public_model.status_commission = True
            else:
                public_model.status_commission = False
            public_model.save()

        public_model.refresh_from_db()

        return f"Task succeeded for {public_model.name}"
    except CommunityModel.DoesNotExist:
        return f"No CommunityModel found for user_id: {user_id}"
    except Exception as e:
        return f"Error: {e}"
