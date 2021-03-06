from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """ User Model Definition """

    avatar = models.ImageField(upload_to="avatars", blank=True)
    is_superhost = models.BooleanField(default=False)
    favs = models.ManyToManyField("rooms.Room", related_name="favs")

    def room_count(self):
        return self.rooms.count()

    room_count.short_description = "Room Count"
