from django.db import models

from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import BaseUserManager

from django.contrib.auth.models import User

# from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Tambahkan kolom baru ke model pengguna
    no_handphone = models.CharField(max_length=20, blank=True)

    # Add other custom fields here


    def __str__(self):
        return self.username

    class Meta:
        # Menentukan nama relasi yang unik untuk grup dan izin pengguna
        # Ini akan menghindari konflik dengan model pengguna bawaan Django
        # Jika kamu tidak menggunakan relasi ini, gunakan nama yang lebih cocok
        # yang tidak akan bertabrakan dengan relasi bawaan Django
        db_table = 'custom_user_table'  # Ganti dengan nama tabel yang sesuai
        managed = True
        default_permissions = ()
        permissions = ()
        unique_together = ()
        swappable = 'AUTH_USER_MODEL'
        # related_name = 'custom_%(app_label)s_%(class)s_related'


# harga paket
class HargaPaket(models.Model):
    nama_paket = models.CharField(max_length=100)
    cpu = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    keterangan = models.TextField(null=True)
    

    def __str__(self):
        return self.nama_paket


# Pesanan Container
class Pesanan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    harga_paket = models.ForeignKey(HargaPaket, on_delete=models.CASCADE)
    core = models.IntegerField()
    ram = models.IntegerField()
    storage = models.IntegerField()
    os = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  # Password akan dienkripsi
    perbulan = models.CharField(max_length=100, null=True)
    jenis = models.CharField(max_length=100, default='container')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


