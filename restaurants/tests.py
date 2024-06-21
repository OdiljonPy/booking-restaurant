from django.db import models
class OrderItems(models.Model):
    menu = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_price(self):
        return self.menu * self.amount

    def __str__(self):
        return self.menu.name

OrderItems.calculate_total_price()

