# Generated by Django 5.0 on 2024-05-26 08:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='comment_text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст комментария'),
        ),
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.BooleanField(null=True, verbose_name='Тип уведомления (усепшный или нет)'),
        ),
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.CharField(max_length=250, null=True, verbose_name='Тема уведомления'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(null=True, verbose_name='Текст уведомления'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='UID'),
        ),
    ]
