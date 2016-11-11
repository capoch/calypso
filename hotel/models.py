from django.db import models
from django.utils import timezone
import datetime

class GuestManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(checkin_date__isnull = False).exclude(checkout_date__lte = timezone.now())
    def future(self):
        return self.get_queryset().filter(checkin_date__gt = timezone.now())

class RoomType(models.Model):

    name = models.CharField(max_length=100)
    description =  models.TextField()
    price = models.IntegerField()


    def __str__(self):
        return self.name

class Motorcycle(models.Model):
    CLUTCH = (
        ('M', 'Manual'),
        ('A', 'Automatic'),
    )
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=30)
    clutch = models.CharField(max_length=1, choices=CLUTCH)
    registration =  models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    date_from = models.DateField()
    date_to = models.DateField(null=True)


    def __str__(self):
        return "{} {} - registration {}".format(self.color, self.model,self.registration)

class Room(models.Model):

    number = models.IntegerField()

    room_type = models.ForeignKey('RoomType')

    def __str__(self):
        return "Room {}".format(self.number)

class Guest(models.Model):

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    checkin_date = models.DateField(name="checkin_date")
    checkout_date = models.DateField(blank=True, null=True, name="checkout_date")
    gender = models.CharField(max_length=1, choices=GENDER)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    passport_number = models.CharField(max_length=20)
    passport_deposited = models.BooleanField(default=False)
    is_guest = models.BooleanField('public', default=True)
    motorcycle = models.ForeignKey('hotel.Motorcycle', on_delete=models.CASCADE, related_name='Guest', blank=True, null=True)
    room = models.ForeignKey('hotel.Room', on_delete=models.CASCADE, related_name='Guest')

    class Meta:
        ordering = ['room']

    objects = GuestManager()

    def __str__(self):
        return "{} in {}".format(self.name, self.room)

class Item(models.Model):
    GROUPS = (
        ('01', 'Drinks'),
        ('02', 'Liquors'),
        ('03', 'Side Orders'),
        ('04', 'Breakfast'),
        ('05', 'Salads'),
        ('06', 'Soups'),
        ('07', 'Sandwiches'),
        ('08', 'Pork'),
        ('09', 'Chicken'),
        ('10', 'Filipino Food'),
        ('11', 'Potato'),
        ('12', 'Pasta'),
        ('13', 'Pork Tenderloin'),
    )
    name = models.CharField(max_length=250)
    group = models.CharField(max_length=2, choices=GROUPS)
    active = models.BooleanField(default=True)
    price = models.IntegerField()

    class Meta:
        ordering = ['group']

    def __str__(self):
        return "{} ({})".format(self.name, self.price)

class Order(models.Model):
    guest = models.ForeignKey('hotel.Guest', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField()
    item = models.ForeignKey('hotel.Item', on_delete=models.CASCADE)
    price = models.IntegerField(default=1)
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['guest']

    def __str__(self):
        return "{} x {}".format(self.amount, self.item)

class RoomItem(models.Model):
     guest = models.ForeignKey('hotel.Guest', on_delete=models.CASCADE)
     room = models.ForeignKey('hotel.Room', on_delete=models.CASCADE)
     date_from = models.DateField()
     date_to = models.DateField()
     price = models.IntegerField()

     class Meta:
         ordering = ['room']

     def __str__(self):
         return "Room:{}, Guest:{} from {} until {}".format(self.Room.number, self.Guest.name, self.date_from, self.date_to)
