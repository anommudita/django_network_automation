from django.contrib import admin

# Register your models here.
from .models import Pesanan, HargaPaket

admin.site.register(Pesanan)
admin.site.register(HargaPaket)

# from users .models import CustomUser

# admin.site.register(CustomUser)