from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.db.models import Max


# Create your models here.
class Post(models.Model):
    text = models.CharField(max_length=200)
    time_str = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200)
    # changed part
    last_changed = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __lt__(self, other):
        return self.create_time.__lt__(other.create_time)

    def __str__(self):
        return self.user_name + " said: " + self.text + " " + self.time_str

    # Return all recent additions and deletions of the posted posts
    @staticmethod
    def get_changes(time="1970-01-01T00:00+00:00"):
        return Post.objects.filter(last_changed__gt=time).distinct()

    # Return all recent additions to the posted posts
    @staticmethod
    def get_posts(time="1970-01-01T00:00+00:00"):
        return Post.objects.filter(deleted=False,
                                   last_changed__gt=time).distinct()

    # Return the modify time of mostly changed post
    @staticmethod
    def get_max_time():
        return Post.objects.all().aggregate(
            Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"


#  Extend abstract User class
class User(AbstractUser):
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)], blank=True, null=True)
    image = models.ImageField(upload_to='profile_image', blank=True,
                              default='/static/imgs/default_photo.jpg')
    bio = models.ImageField(blank=True, max_length=420)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta(AbstractUser.Meta):
        pass


# Model to represent each email verification record
class EmailVerifyRecord(models.Model):
    email = models.EmailField(null=False)
    code = models.CharField(max_length=64, null=False)
    type = models.CharField(max_length=50, default="")


# Model to represent each comment of the posts
# One post could have several comments
# One user could send several comments
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    time_str = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)