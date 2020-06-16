from djongo import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime

class User(AbstractUser):
    email = models.EmailField(null=True)

class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    url = models.CharField(max_length=200, null=True)
    content = models.TextField(default='')
    is_multi_page = models.BooleanField()
    page_id = models.CharField(max_length=50, null=True)
    next_check = models.FloatField(default=0)