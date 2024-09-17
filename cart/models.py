from django.db import models
from django.contrib.auth.models import User
from orders.models import OrderItem

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderItem)

    def __str__(self):
        return str(self.id)
