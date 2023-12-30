from django.db import models

class TypeButton(models.Model):
    name_button = models.CharField(max_length=100, verbose_name="Тип кнопки")

    def __str__(self):
        return self.name_button
    
    class Meta:
        verbose_name = "Кнопка"
        verbose_name_plural = "Кнопки"


class AddSingleCreative(models.Model):
    button = models.ForeignKey(
        TypeButton,
        on_delete=models.CASCADE,
        verbose_name="Тип кнопки"
        )
    # file = models.FileField(verbose_name="Файл для креатива", upload_to='files')
    link = models.CharField(max_length=500, verbose_name="Ссылка")
    name = models.CharField(max_length=200, verbose_name="Название")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Креатив"
        verbose_name_plural = "Креативы"


class AddDoubleCreative(models.Model):
    button = models.ForeignKey(
        TypeButton,
        on_delete=models.CASCADE,
        verbose_name="Тип кнопки"
        )
    
    # first_file = models.FileField(verbose_name="Первый файл для креатива", upload_to='files')
    first_link = models.CharField(max_length=500, verbose_name="Первая ссылка")
    first_name = models.CharField(max_length=200, verbose_name="Первое название")

    # second_file = models.FileField(verbose_name="Второй файл для креатива", upload_to='files')
    second_link = models.CharField(max_length=500, verbose_name="Вторая ссылка")
    second_name = models.CharField(max_length=200, verbose_name="Второе название")

    def __str__(self):
        return self.first_name
    
    class Meta:
        verbose_name = "Двойной креатив"
        verbose_name_plural = "Двойные креативы"


class RepostCreative(models.Model):
    link_of_story = models.CharField(max_length=150, verbose_name="Ссылка на историю")
    name = models.CharField(max_length=150, verbose_name="Название")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Репост"
        verbose_name_plural = "Репосты"


class StickerCreative(models.Model):
    link_of_story = models.CharField(max_length=150, verbose_name="Ссылка на историю")
    name = models.CharField(max_length=150, verbose_name="Название")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Ссылка-стикер"
        verbose_name_plural = "Ссылка-стикеры"


class DoubleStickerCreative(models.Model):
    link_of_story_first = models.CharField(max_length=150, verbose_name="Ссылка на историю №1")
    link_of_story_second = models.CharField(max_length=150, verbose_name="Ссылка на историю №2")
    name = models.CharField(max_length=150, verbose_name="Название")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Двойная ссылка-стикер"
        verbose_name_plural = "Двойные ссылка-стикеры"