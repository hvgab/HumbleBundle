from operator import mod
from pyexpat import model
from statistics import mode
from django.db import models

# Create your models here.

class Game(models.Model):
    platform = models.CharField(max_length=32, blank=True, null=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    paragraph = models.CharField(max_length=256, blank=True, null=True)
    game_link_text = models.CharField(max_length=256, blank=True, null=True)
    game_link_href = models.URLField(blank=True, null=True)
    choice_url = models.URLField(blank=True, null=True)
    is_redeemed = models.BooleanField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'game_link_href'], name='unique title href')
        ]

    def __str__(self) -> str:
        return self.title

