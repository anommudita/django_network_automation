from django.urls import path

from . import views

urlpatterns = [
    # route login dan login
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),


    # halaman utama dan dashboard
    path('', views.home, name="home"),
    path('createcluster', views.createCluster, name="createcluster"),
    path('joincluster', views.joinCluster, name="joincluster"),

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
    path('detail-node/<str:id_node>', views.detail_node, name="detail-node"),

    # route reboot node
    path('nodes/<str:id_node>/reboot', views.rebootNode, name="reboot-node"),
    #route shutdown node
    path('nodes/<str:id_node>/shutdown', views.shutdownNode, name="shutdown-node"),

    # route node network
    path('node-network/<str:id_node>', views.networkNode, name="node-network"),

    #  route add network linux bridge
    path('add-linux-bridge/<str:id_node>/<str:type>', views.addLinuxBridge, name="add-linux-bridge"),



    # route add container
    path('add-container/<str:id_node>', views.addContainer, name="add-container"),

    # route remove container

    # route start container
    path('start-container/<str:id_node>/<str:vmid>', views.startContainer, name="start-container"),
    # route stop container 
    path('stop-container/<str:id_node>/<str:vmid>', views.stopContainer, name="stop-container"),
    # route reboot container 
    path('reboot-container/<str:id_node>/<str:vmid>', views.rebootContainer, name="reboot-container"),


    # route add virtual_machine 

    # route remove virtual_machine

    # route start virtual_machine
    path('start-virtual_machine/<str:id_node>/<str:vmid>', views.startVirtualMachine, name="start-virtual_machine"),
    # route stop virtual_machine 
    path('stop-virtual_machine/<str:id_node>/<str:vmid>', views.stopVirtualMachine, name="stop-virtual_machine"),
    # route reboot virtual_machine 
    path('reboot-virtual_machine/<str:id_node>/<str:vmid>', views.rebootVirtualMachine, name="reboot-virtual_machine"),

    # route detail container
    path('detail-container/<str:id_node>/<str:vmid>', views.detail_container, name="detail-container"),

    # route cluster
    path('clusters', views.clusters, name="clusters"),


    # route monitoring
    path('monitors', views.monitors, name="monitors"),

    # route profile
    path('profile', views.profile, name="profile"),
    # route edit profile
    path('edit-profile', views.edit_profile, name="edit-profile"),
    # route update-image
    path('image-update', views.updateImage, name="image-update"),


    # route settings
    path('settings', views.settings, name="settings"),


    # route config
    path('config', views.config, name="config"),
    # route config_by_user
    path('config_by_user', views.config_by_user, name="config_by_user"),


]