from django.contrib import admin

from .models import Room, RoomType, Guest, Item, Order, Motorcycle
# Register your models here.
admin.site.register(RoomType)

admin.site.register(Room)

admin.site.register(Guest)

admin.site.register(Item)

admin.site.register(Order)

admin.site.register(Motorcycle)
