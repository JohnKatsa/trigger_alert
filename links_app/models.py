from djongo import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(null=True)

class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    url = models.CharField(max_length=200, null=True)
    is_multi_page = models.BooleanField()
    page_id = models.CharField(max_length=50, null=True)