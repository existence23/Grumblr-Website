from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Post(models.Model):
    text = models.CharField(max_length=200)
    # user_name = models.CharField(max_length=200)
    time_str = models.CharField(max_length=200)
    creat_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200)

    def __lt__(self, other):
        return self.time.__lt__(other.time)

    def __str__(self):
        return self.user_name + " said: " + self.text + " " + self.time
