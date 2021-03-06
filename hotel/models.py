from django.db import models
from django.utils import timezone
import datetime
from model_utils import FieldTracker


class GuestManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(checkin_date__lte = timezone.now()).exclude(checkout_date__lte = timezone.now())
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
    date_to = models.DateField(null=True, blank=True)


    def __str__(self):
        return "{} {} - registration {}".format(self.color, self.model,self.registration)

class Room(models.Model):

    number = models.IntegerField()

    room_type = models.ForeignKey('RoomType')

    def __str__(self):
        return "Room {}".format(self.number)

class Guest(models.Model):

    checkin_date = models.DateField(name="checkin_date")
    checkout_date = models.DateField(blank=True, null=True, name="checkout_date")
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    passport_number = models.CharField(max_length=20)
    passport_deposited = models.BooleanField(default=False)
    is_guest = models.BooleanField('public', default=True)
    motorcycle = models.ForeignKey('hotel.Motorcycle', on_delete=models.CASCADE, related_name='Guest', blank=True, null=True)
    room = models.ForeignKey('hotel.Room', on_delete=models.CASCADE, related_name='Guest')
    discount = models.FloatField(default=0, verbose_name='Discount in %')

    class Meta:
        ordering = ['room']

    objects = GuestManager()

    def __str__(self):
        return self.name

    checkout_tracker = FieldTracker(fields=['checkout_date'])


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
        ('98', 'Room'),
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
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return "{} x {}".format(self.amount, self.item)

class RoomItem(models.Model):
     guest = models.ForeignKey('hotel.Guest', on_delete=models.CASCADE)
     room = models.ForeignKey('hotel.Room', on_delete=models.CASCADE)
     date_from = models.DateField()
     date_to = models.DateField(null=True)
     days_paid = models.IntegerField(default=0)
     price = models.IntegerField(null=True)

     class Meta:
         ordering = ['room']

     def __str__(self):
         return "{} in {} from {} until {}".format(self.guest, self.room, self.date_from, self.date_to)

class Occupation(models.Model):
    room = models.ForeignKey('hotel.Room', on_delete=models.CASCADE)
    #maybe quest belongs in here too
    date = models.DateField()
    is_occupaid = models.BooleanField(default=False)

    def __str__(self):
        return "{} for Room {}".format(self.date, self.room)

class StockItem(models.Model):
    item = models.ForeignKey('hotel.Item', on_delete=models.CASCADE)
    in_stock = models.IntegerField()
    daily_use_avg = models.FloatField()
    last_buy = models.DateField()
    warning = models.IntegerField(default=0)

    def __str__(self):
        return "{} of {}".format(self.in_stock, self.item)

class Complaint(models.Model):
    SEVERITY = (
        ('00', 'note'),
        ('01', 'low'),
        ('02', 'medium'),
        ('03', 'high'),
    )
    CATEGORY = (
        ('00', 'general'),
        ('01', 'sanitary'),
        ('02', 'electric'),
        ('03', 'windows/doors'),
        ('04', 'animals')
    )
    room = models.ForeignKey('hotel.Room', on_delete=models.CASCADE)
    date_reported = models.DateField()
    date_fixed = models.DateField(blank=True, null=True)
    responsible = models.ForeignKey('hotel.Employee')
    severity = models.CharField(max_length=2, choices=SEVERITY)
    category = models.CharField(max_length=2, choices=CATEGORY)
    comments = models.CharField(max_length=250)

class Employee(models.Model):
    LEVEL = (
        ('00', 'Owner'),
        ('01', 'Management'),
        ('02', 'Staff'),
        ('03', 'External'),
    )
    name = models.CharField(max_length=30)
    level = models.CharField(max_length=2, choices=LEVEL)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}({})".format(self.name, self.level)
