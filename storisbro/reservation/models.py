from django.db import models

# Модель места брони
class DateOfReservation(models.Model):
    """Модель по созданию объектов брони. Дата и количество свободных мест."""
    date = models.DateField(verbose_name="Дата брони")
    count_room = models.PositiveSmallIntegerField(verbose_name="Количество свободных мест")

    class Meta:
        verbose_name = "Место брони"
        verbose_name_plural = "Места брони"

    def __str__(self):
        return f"{self.date} - {self.count_room} свободных мест"    


# Тестовая модель креатива
class CreativeModel(models.Model):
    date = models.ForeignKey(
        DateOfReservation,
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Дата брони")
    name = models.CharField(max_length=200, verbose_name="Название креатива")
    link = models.URLField(verbose_name="Ссылка на объект рекламирования")
    status = models.BooleanField(default=True, verbose_name="Статус брони")
    commentary = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Креатив"
        verbose_name_plural = "Креативы"
    
