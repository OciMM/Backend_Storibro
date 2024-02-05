from django.db import models
from django.conf import settings

# class PublicModel(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     name = models.CharField(max_length=150, verbose_name="ID сообщества")
#     url = models.URLField(unique=True, verbose_name="Ссылка которая должна быть в сообществе")
#     status = models.BooleanField(default=False, verbose_name="Статус ссылки")

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Сообщество"
#         verbose_name_plural = "Сообщества"

