from django.contrib import admin

# Register your models here.
from .models import Server, UserProfile

admin.site.register(Server)
admin.site.register(UserProfile)