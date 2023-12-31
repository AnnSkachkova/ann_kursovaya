from django.contrib import admin
from . import models


@admin.register(models.Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['token', 'user']
    list_display_links = ['token', 'user']
    
    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'price', 'photo', 'dt_created', 'dt_updated', 'to_remove']
    list_display_links = ['title', 'description', 'price', 'photo']
    

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
    

@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'destination_type', 'apply_flag', 'contractor', 'dt_created', 'dt_updated', 'to_remove']
    list_display_links = ['destination_type', 'contractor']
    

@admin.register(models.DocumentItem)
class DocumentItemAdmin(admin.ModelAdmin):
    list_display = ['document', 'product', 'count']
    list_display_links = ['product']