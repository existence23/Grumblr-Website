from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


# Create your models here.
class Post(models.Model):
    text = models.CharField(max_length=200)
    time_str = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200)

    def __lt__(self, other):
        return self.create_time.__lt__(other.create_time)

    def __str__(self):
        return self.user_name + " said: " + self.text + " " + self.time


class User(AbstractUser):
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)], blank=True, null=True)
    image = models.ImageField(upload_to='profile_image', blank=True,
                              default='/static/imgs/default_photo.jpg')
    bio = models.ImageField(blank=True, max_length=420)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta(AbstractUser.Meta):
        pass


class EmailVerifyRecord(models.Model):
    email = models.EmailField(null=False)
    code = models.CharField(max_length=64, null=False)
    type = models.CharField(max_length=50, default="")

