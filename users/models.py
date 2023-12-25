from django.db import models

# # membuat user akun menggunakan bawaan django!
# from django.contrib.auth.models import User
# class UserClient(models.Model):
#     # user
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_client')

#     # name
#     name = models.CharField(max_length=250)
#     no_hp = models.CharField(max_length=250)

#     date_created = models.DateTimeField(blank=True, null= True)
#     update_created = models.DateTimeField(blank=True, null= True)

#     # avatar
#     # avatar = models.ImageField(blank = True, null = True, upload_to='images/')

#     def  __str__(self):
#             return self.user.username
    
#     def save_user_client(sender, instance, created, **kwargs):
#         print(instance)
#         try:
#             user_client = UserClient.objects.get(user=instance)
#         except Exception as e:
#             UserClient.objects.create(user=instance)
#         instance.user_client.save()



# from django.contrib.auth.models import User
# from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver


# class UserClient(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_client')
#     name = models.CharField(max_length=250)
#     no_hp = models.CharField(max_length=250)
#     date_created = models.DateTimeField(auto_now_add=True)
#     update_created = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.user.username


# @receiver(post_save, sender=User)
# def create_user_client(sender, instance, created, **kwargs):
#     if created:
#         UserClient.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_client(sender, instance, **kwargs):
#     instance.user_client.save()




from django.contrib.auth.models import AbstractUser


from django.contrib.auth.models import BaseUserManager

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




