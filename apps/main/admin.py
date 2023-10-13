from django.contrib import admin
from . import models


@admin.register(models.Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['token', 'user']
    list_display_links = ['token', 'user']
    