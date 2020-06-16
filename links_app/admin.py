from django.contrib import admin
from links_app import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Link)