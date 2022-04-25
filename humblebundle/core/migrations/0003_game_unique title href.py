# Generated by Django 4.0.4 on 2022-04-25 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_game_choice_url_alter_game_game_link_href_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='game',
            constraint=models.UniqueConstraint(fields=('title', 'game_link_href'), name='unique title href'),
        ),
    ]
