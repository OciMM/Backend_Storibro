# Generated by Django 5.0 on 2023-12-28 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DateOfReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата брони')),
                ('count_room', models.PositiveSmallIntegerField(verbose_name='Количество свободных мест')),
            ],
            options={
                'verbose_name': 'Место брони',
                'verbose_name_plural': 'Места брони',
            },
        ),
        migrations.CreateModel(
            name='CreativeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название креатива')),
                ('link', models.URLField(verbose_name='Ссылка на объект рекламирования')),
                ('date', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.dateofreservation', verbose_name='Дата брони')),
            ],
            options={
                'verbose_name': 'Креатив',
                'verbose_name_plural': 'Креативы',
            },
        ),
    ]
