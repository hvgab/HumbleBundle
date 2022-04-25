from django.contrib import admin
from .models import Game

# Register your models here.
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_filter = ['platform', 'choice_url', 'is_redeemed']
    list_display = ['platform', 'title', 'is_redeemed']
    search_fields = ['title']
    list_display_links = ['title']