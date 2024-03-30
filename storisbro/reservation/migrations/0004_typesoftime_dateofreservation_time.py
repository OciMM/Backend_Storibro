# Generated by Django 5.0 on 2024-02-23 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_delete_creativemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypesOfTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(verbose_name='время публикации')),
            ],
        ),
        migrations.AddField(
            model_name='dateofreservation',
            name='time',
            field=models.ManyToManyField(blank=True, to='reservation.typesoftime', verbose_name='Время публикации'),
        ),
    ]
