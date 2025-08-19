from django.contrib import admin
from .models import Item, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'currency', 'price')
	search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'currency', 'total_price', 'discount_percent', 'tax_percent')
	filter_horizontal = ('items',)
