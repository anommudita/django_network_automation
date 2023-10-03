from django.urls import path

from . import views


urlpatterns = [

    # halaman utama
    path('', views.home, name="home"),


    # route user
    path('user', views.user, name="user"),

    path('adduser', views.addUser, name="adduser"),


    # tampilan edit user
    path('edit-user/<int:id>', views.editUser, name="edit-user"),

    # logic update user
    path('update-user/<int:id>', views.updateUser, name="update-user"),

    # logic update user
    path('delete-user/<int:id>', views.deleteUser, name="delete-user"),
]