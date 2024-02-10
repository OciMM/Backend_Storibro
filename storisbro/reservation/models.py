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

 