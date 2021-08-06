# Generated by Django 3.2.6 on 2021-08-06 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discovery', '0015_remove_profile_invitation_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitedusers',
            name='user',
        ),
        migrations.AddField(
            model_name='invitedusers',
            name='email',
            field=models.EmailField(default='test@test.test', max_length=254, verbose_name='Email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invitedusers',
            name='initial_tags',
            field=models.ManyToManyField(to='discovery.Tag', verbose_name='Initial tags'),
        ),
        migrations.AddField(
            model_name='invitedusers',
            name='is_registered',
            field=models.BooleanField(default=False, verbose_name='Registered'),
        ),
        migrations.AlterField(
            model_name='invitedusers',
            name='inviter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Inviter'),
        ),
    ]
