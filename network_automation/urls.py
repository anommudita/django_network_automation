from django.urls import path

from . import views


urlpatterns = [


    # route login dan login
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),


    # halaman utama dan dashboard
    path('', views.home, name="home"),
    path('cluster-resources/', views.cluster_resources, name='cluster-resources'),
    path('cluster-log/', views.cluster_log, name='cluster-log'),

    # route error
    path('error', views.error_connection, name="error_connection"),

    # route data api
    path('data_api', views.data_api, name="data_api"),


    # route user
    path('user', views.user, name="user"),
    path('adduser', views.addUser, name="adduser"),
    path('edit-user/<str:id>', views.updateUser, name="edit-user"),
    path('delete-user/<str:userid>', views.deleteUser, name="delete-user"),


    # route groups
    path('groups', views.groups, name="groups"),
    path('addgroup', views.addGroup, name="addgroup"),
    path('delete-group/<str:groupid>', views.deleteGroup, name="delete-group"),
    path('edit-group/<str:groupid>', views.updateGroup, name="edit-group"),

    # route permission
    path('permissions', views.permissions, name="permissions"),
    path('delete-permissions/<path:path>/<str:roles>/<str:type>/<str:ugid>', views.deletePermissions, name="delete-permissions"),
    # add permission group
    path('add-permission-group', views.addPermissionGroup, name="add-permission-group"),
    # add permission user
    path('add-permission-user', views.addPermissionUser, name="add-permission-user"),
    # add permissions api
    path('add-permission-api', views.addPermissionAPI, name="add-permission-api"),

    # route roles
    path('roles', views.roles, name="roles"),
    path('addrole', views.addRole, name="addrole"),
    path('edit-role/<str:roleid>', views.updateRole, name="edit-role"),
    path('delete-role/<str:roleid>', views.deleteRole, name="delete-role"),

    # route node
    path('nodes', views.nodes, name="nodes"),


    # route cluster
    path('clusters', views.clusters, name="clusters"),


    # route monitoring
    path('monitors', views.monitors, name="monitors"),

    # route profile
    path('profile', views.profile, name="profile"),


    # route settings
    path('settings', views.settings, name="settings"),


    # route config
    path('config', views.config, name="config"),





]