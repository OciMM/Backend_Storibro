# Generated by Django 5.0 on 2024-02-23 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_user_vk_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя пользователя'),
        ),
    ]