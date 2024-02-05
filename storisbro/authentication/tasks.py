from celery import shared_task
from django.core.mail import send_mail

from authentication.models import User


@shared_task
def user_created(user_id, confirmation_code):
    user = User.objects.get(id=user_id)
    subject = 'Приветствую в нашей социальной сети'
    message = f'Дорогой пользователь,\n\n' \
              f'Пожалуйста, подтвердите вашу почту, используя следующий код: {confirmation_code}.'
    mail_sent = send_mail(subject, message, 'bekasovmaks20@gmail.com', [user.email])
    return mail_sent


@shared_task
def user_login_code(user_id, confirmation_code):
    user = User.objects.get(id=user_id)
    subject = 'Приветствую в нашей социальной сети'
    message = f'Дорогой пользователь,\n\n' \
              f'Пожалуйста, подтвердите вашу почту для входа, используя следующий код: {confirmation_code}.'
    mail_sent = send_mail(subject, message, 'bekasovmaks20@gmail.com', [user.email])
    return mail_sent
