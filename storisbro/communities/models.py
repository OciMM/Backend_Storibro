from django.db import models
from django.conf import settings


class StatusCommunities(models.Model):
    status = models.CharField(max_length=300, verbose_name="Статус проверки")

    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name = "Статус проверки сообщества"
        verbose_name_plural = "Статусы проверки сообществ"


class CommunityModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=350, verbose_name="Имя сообщества")
    # photo = models.URLField(verbose_name="Ссылка аватарки", null=True) # потом надо поменять на FileField
    url = models.URLField(verbose_name="Ссылка сообщества")

    status_of_check = models.ForeignKey(
        StatusCommunities,
        on_delete=models.PROTECT,
        default=1,
        verbose_name="Статус"
    )

    # name_id_commission = models.CharField(max_length=150, verbose_name="ID сообщества", blank=True, null=True)
    status_commission = models.BooleanField(default=False, verbose_name="Статус ссылки")
    url_commission =  models.URLField(
        verbose_name="Ссылка которая должна быть в сообществе", 
        blank=True, 
        default="https://www.shopify.com/blog/low-investment-business-ideas"
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Сообщество"
        verbose_name_plural = "Сообщества"


class Setting(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название настройки")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Вид настройки"
        verbose_name_plural = "Виды настроек"


class CommunitySetting(models.Model):
    community = models.ForeignKey(CommunityModel, on_delete=models.CASCADE, verbose_name="Сообщество")
    status = models.ForeignKey(Setting, on_delete=models.CASCADE, verbose_name="Вид настройки")
    link_to_telegram = models.URLField(blank=True, null=True, verbose_name="Ссылка на телеграм канал")

    def __str__(self):
        return self.link_to_telegram
    
    class Meta:
        verbose_name = "Настройки сообщества"
        verbose_name_plural = "Настройки сообществ"

