# Generated by Django 5.0 on 2024-02-18 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistics_for_admin_site', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='registered_users_client',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistics',
            name='registered_users_owner',
            field=models.IntegerField(default=0),
        ),
    ]
