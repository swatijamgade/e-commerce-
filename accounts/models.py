from django.db import models
from django.contrib.auth.models import User, Group, Permission


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/images/%Y/%m/%d', blank=True)
    mobile = models.CharField(max_length=10)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='addresses')
    type = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    pin_code = models.CharField(max_length=6)

    def __str__(self):
        return self.type


class Roles(models.Model):
    ROLE_CHOICE = (
        ('ADMIN', 'ADMIN'),
        ('USER', 'USER'),
    )
    role = models.CharField(max_length=128, choices=ROLE_CHOICE)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.role