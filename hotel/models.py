from django.db import models

class RoomType(models.Model):

    name = models.CharField(max_length=100)
    description =  models.TextField()

    def __str__(self):
        return self.name

class Room(models.Model):

    number = models.IntegerField()

    room_type = models.ForeignKey('RoomType')

    def __str__(self):
        return str(self.number), self.room_type

##class Guest(models.Model):

#    name = models.CharField(max_length=30)

#    room = models.ForeignKey('Room')

# Create your models here.
