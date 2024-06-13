from django.db import models
from django.contrib.auth.models import User
from restaurants.models import Restaurant


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
# Create your models here.
