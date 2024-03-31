from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Register(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    mobile = models.CharField(max_length=10,null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=10,null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
class Station(models.Model):
    station_name = models.CharField(max_length=100,null = True)
    station_city = models.CharField(max_length = 100,null = True)

class Train(models.Model):
    trainname = models.CharField(max_length=30,null=True)
    # train_no = models.IntegerField(null=True)
    from_station = models.ForeignKey(Station, on_delete=models.SET_NULL, related_name='from_city', null=True)
    to_station = models.ForeignKey(Station, on_delete=models.SET_NULL, related_name='to_city', null=True)
    departuretime=models.CharField(max_length=30,null=True)
    arrivaltime=models.CharField(max_length=30,null=True)
    traveltime=models.CharField(max_length=100,null=True)
    distance=models.IntegerField(null=True)
    # img=models.FileField(null=True)
    stations = models.ManyToManyField(Station,through='Route')
    fare = models.DecimalField(max_digits=10, decimal_places = 2) 
    train_image = models.ImageField(upload_to='train_images/', null=True, blank=True)


class Route(models.Model):
    train = models.ForeignKey(Train,on_delete=models.CASCADE)
    station = models.ForeignKey(Station,on_delete=models.CASCADE)
    traveltime=models.CharField(max_length=100,null=True)
    distance=models.IntegerField(null=True)
    fare = models.DecimalField(max_digits=10, decimal_places = 2)

class Passenger(models.Model):
    user = models.ManyToManyField(User)
    train = models.ForeignKey(Train,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,null=True)
    age = models.IntegerField(null=True)
    date = models.DateField(null=True)

class Ticket(models.Model):
    passenger=models.ForeignKey(Passenger,on_delete=models.CASCADE,null=True)
    from_station=models.CharField(max_length=100,null = True)
    to_station = models.CharField(max_length = 100,null = True)
    fare=models.IntegerField(null=True)


