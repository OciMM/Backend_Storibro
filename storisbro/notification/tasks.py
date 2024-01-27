from celery import shared_task
from django.core.mail import send_mail
import vk_api

from urllib.parse import urlparse, parse_qs
from authentication.models import User
from notification.models import Notification


@shared_task
def send_notification(user_id, message):
    try:
        redirect_uri_with_token = 'https://example.com/callback#access_token=ваш_токен_доступа&expires_in=86400&user_id=ваш_идентификатор_пользователя&state=your_state'
        parsed_url = urlparse(redirect_uri_with_token)
        token = parse_qs(parsed_url.fragment)['access_token'][0]

        vk_session = vk_api.VkApi(token=token)
        vk = vk_session.get_api()

        group_id = 223942700 # потом тут надо поставить реальный id

        vk.messages.allowMessagesFromGroup(
            group_id=group_id
        )

        # Email notification
        send_mail(
            'Notification',
            message,
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )

        try:
            user = User.objects.get(id=user_id)
            notification = Notification(user=user, message=message)
            notification.save()
            print(f"Профиль пользователя {user.email} успешно обновлен с уведомлением: {message}")
        except User.DoesNotExist:
            print(f"Пользователь с id={user_id} не найден.")
        except Exception as e:
            print(f"Ошибка при обновлении профиля пользователя: {e}")

    except vk_api.ApiError as e:
        print(f"VK API Error: {e}")
    except Exception as e:
        print(f"Error: {e}")