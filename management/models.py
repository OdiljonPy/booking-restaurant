from django.db import models
from authentication.models import User
from restaurants.models import Restaurant


class Manager(models.Model):
    manager = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

