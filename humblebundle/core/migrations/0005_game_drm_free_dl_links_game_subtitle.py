# Generated by Django 4.0.4 on 2022-04-25 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_game_game_link_href'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='drm_free_dl_links',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='subtitle',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
