# Generated by Django 5.0 on 2024-01-07 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creatives', '0004_alter_doublestickercreative_link_of_story_first_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusCreative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100, verbose_name='Статус проверки')),
            ],
            options={
                'verbose_name': 'Статус проверки креатива',
                'verbose_name_plural': 'Статусы проверки креативов',
            },
        ),
    ]
