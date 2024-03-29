# Generated by Django 5.0 on 2024-02-08 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creatives', '0010_addsinglecreative_reservation'),
        ('reservation', '0003_delete_creativemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='addsinglecreative',
            name='date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата добавления креатива'),
        ),
        migrations.AlterField(
            model_name='addsinglecreative',
            name='reservation',
            field=models.ManyToManyField(blank=True, to='reservation.dateofreservation', verbose_name='Бронирование'),
        ),
    ]
