from django.db import models

class UserModel(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя пользователя")
    status = models.BooleanField(default=False, verbose_name="Статус пониженной комиссии")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class PublicModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, verbose_name="Имя сообщества")
    url = models.URLField(unique=True, verbose_name="Ссылка группы")
    status = models.BooleanField(default=False, verbose_name="Статус ссылки")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сообщество"
        verbose_name_plural = "Сообщества"

