# Generated by Django 5.0 on 2024-05-26 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_notification_comment_text_notification_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.BooleanField(blank=True, null=True, verbose_name='Тип уведомления (усепшный или нет)'),
        ),
    ]