# Generated by Django 3.2.4 on 2021-09-06 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20210831_0534'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatsessionuser',
            name='is_tagged',
            field=models.BooleanField(default=False),
        ),
    ]