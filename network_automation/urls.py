from django.urls import path

from . import views


urlpatterns = [

    # halaman utama
    path('', views.home, name="home"),


    # route user
    path('user', views.user, name="user"),


    path('adduser', views.addUser, name="adduser"),

    # route data api
    path('data_api', views.data_api, name="data_api"),


    # route error
    path('error', views.error_connection, name="error_connection"),

    # route groups
    path('groups', views.groups, name="groups"),
    path('addgroup', views.addGroup, name="addgroup"),
    path('delete-group/<str:groupid>', views.deleteGroup, name="delete-group"),
    path('edit-group/<str:groupid>', views.updateGroup, name="edit-group"),

    # route permission
    path('permissions', views.permissions, name="permissions"),

    # route roles
    path('roles', views.roles, name="roles"),


    # tampilan edit user
    path('edit-user/<int:id>', views.editUser, name="edit-user"),

    # logic update user
    path('update-user/<int:id>', views.updateUser, name="update-user"),

    # logic update user
    path('delete-user/<str:userid>', views.deleteUser, name="delete-user"),
]