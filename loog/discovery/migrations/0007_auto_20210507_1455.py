# Generated by Django 3.2.2 on 2021-05-07 14:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0006_alter_profile_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usertag',
            old_name='tag_id',
            new_name='tag',
        ),
        migrations.AddField(
            model_name='usertag',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]