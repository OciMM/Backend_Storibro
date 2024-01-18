from django.db import models


class StatusCommunities(models.Model):
    status = models.CharField(max_length=100, verbose_name="Статус проверки")

    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name = "Статус проверки сообщества"
        verbose_name_plural = "Статусы проверки сообществ"


class CommunityModel(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя сообщества")
    photo = models.URLField(verbose_name="Ссылка аватарки") # потом надо поменять на FileField
    url = models.URLField(verbose_name="Ссылка сообщества")

    status_of_check = models.ForeignKey(
        StatusCommunities,
        on_delete=models.PROTECT,
        default=1,
        verbose_name="Статус"
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

