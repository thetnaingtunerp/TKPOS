from django.contrib import admin
from .models import *
# Register your models here.
# list view of items in admin panel
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
admin.site.register(Item, ItemAdmin)