from django.db import models


class User(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя пользователя")
    email = models.EmailField(verbose_name="Электронная почта пользователя")
    account_vk = models.CharField(max_length=150, verbose_name="VK ID пользователя")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Пользователь для теста"
        verbose_name_plural = "Пользователи для теста"
