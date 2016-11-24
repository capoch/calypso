from django.contrib import admin

from .models import Room, RoomType, Guest, Item, StockItem, Order, Motorcycle, RoomItem, Occupation
# Register your models here.
admin.site.register(RoomType)

admin.site.register(Room)

admin.site.register(Guest)

admin.site.register(Item)

admin.site.register(StockItem)

admin.site.register(Order)

admin.site.register(Motorcycle)

admin.site.register(RoomItem)

admin.site.register(Occupation)
