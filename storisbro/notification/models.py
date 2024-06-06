from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    Это модель уведомления.
    На основе этой модели будут отправляться сообщения в личный кабинет.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, to_field='UID')
    title = models.CharField(max_length=250, verbose_name="Тема уведомления", null=True)
    message = models.TextField(verbose_name="Текст уведомления", null=True)
    comment_text = models.TextField(verbose_name="Текст комментария", blank=True, null=True)
    status = models.BooleanField(verbose_name="Тип уведомления (усепшный или нет)", blank=True, null=True)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    file = models.FileField(verbose_name="Файл для креатива", upload_to='files', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'