from django.contrib import admin

from .models import Room, RoomType
# Register your models here.
admin.site.register(RoomType)

admin.site.register(Room)
