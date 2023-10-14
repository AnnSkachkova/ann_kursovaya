from django.contrib import admin
from . import models


@admin.register(models.Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['token', 'user']
    list_display_links = ['token', 'user']
    
    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'price', 'dt_created', 'dt_updated', 'to_remove']
    list_display_links = ['title', 'description', 'price']
    

@admin.register(models.Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'dt_created', 'dt_updated', 'to_remove']
    list_display_links = ['title']
    

@admin.register(models.Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['username', 'operation', 'dt_created']


@admin.register(models.StorageItem)
class StorageItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'count', 'dt_created', 'dt_updated', 'to_remove']
    list_display_links = ['product']