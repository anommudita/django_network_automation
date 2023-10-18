from django.db import models

# membuat user akun menggunakan bawaan django!
from django.contrib.auth.models import User

# Create your models here.

# table server
class Server(models.Model):
    ip_address = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    # class Meta:
        # nama table ketika untuk mysql
        # db_table = "server"

    def  __str__(self):
        return self.ip_address
    

