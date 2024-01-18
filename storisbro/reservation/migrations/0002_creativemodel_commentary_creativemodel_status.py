# Generated by Django 5.0 on 2024-01-15 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='creativemodel',
            name='commentary',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='creativemodel',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Статус брони'),
        ),
    ]
