from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    file = models.FileField(upload_to='files')
    mobile = models.CharField(max_length=10)
    address = models.TextField()


# prof = Profile.objects.get(id=1)
# prof.image
# prof.mobile
# prof.user.username
# prof.user.email
#
# user = User.objects.get(id=1)
# user.profile.image
# user.profile.mobile
#
# c = Comment.objects.get(id=1)
# c.post.author
# c.post.title
# c.post.publish


class Car:
    pass


red_car = Car()
type(red_car)
age = 100
type(age)