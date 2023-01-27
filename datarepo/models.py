from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.IntegerField(null=True, blank=True)


class Newsfeed(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    news = models.CharField(max_length=255, null=True, blank=True, default=None)
