from django.urls import path

from network_automation import views

urlpatterns = [
    # route login dan login
    path('login/', views.login, name="login"),
    path('logout', views.logout, name="logout"),

    # halaman utama dan dashboard
    path('', views.home, name="proxmox"),
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

    #route delnode
    path('nodes/delnode/<str:node_name>', views.deleteNode, name="delete-nodes"),

    # install ceph
    path('detail-node/<str:id_node>/install-ceph', views.installCeph, name="install-ceph"),
    path('detail-node/<str:id_node>/install-iptables', views.installIptables, name="install-iptables"),

    # add pre and post route port forwarding
    path('pre-route/<str:id_node>', views.preRoute, name="pre-route"),
    path('post-route/<str:id_node>', views.postRoute, name="post-route"),

    path('exec-paramiko/<str:id_node>', views.get_exec_paramiko, name="exec-paramiko"),

    # route reboot node
    path('nodes/<str:id_node>/reboot', views.rebootNode, name="reboot-node"),
    #route shutdown node
    path('nodes/<str:id_node>/shutdown', views.shutdownNode, name="shutdown-node"),

    # route node network
    path('node-network/<str:id_node>', views.networkNode, name="node-network"),

    # route install ovs node
    path('install-ovs/<str:id_node>', views.install_ovs_switch, name="install-ovs"),

    #  route add network linux bridge
    path('add-linux-bridge/<str:id_node>', views.addLinuxBridge, name="add-linux-bridge"),

    #  route add network linux Bond
    path('add-linux-bond/<str:id_node>', views.addLinuxBond, name="add-linux-bond"),

    #  route add network linux Vlan
    path('add-linux-vlan/<str:id_node>', views.addLinuxVlan, name="add-linux-vlan"),

    #  route add network ovs bridge
    path('add-ovs-bridge/<str:id_node>', views.addOVSBridge, name="add-ovs-bridge"),

    #  route add network ovs bond
    path('add-ovs-bond/<str:id_node>', views.addOVSBond, name="add-ovs-bond"),

    #  route add network ovs intport
    path('add-ovs-intport/<str:id_node>', views.addOVSIntPort, name="add-ovs-intport"),
    
    # route network apply
    path('apply-network/<str:id_node>', views.NetworkApply, name="apply-network"),
    
    # route delete network
    path('delete-network/<str:iface>/<str:id_node>', views.deleteNetwork, name="delete-network"),

    # route add container
    path('add-container/<str:id_node>', views.addContainer, name="add-container"),

    # route remove container
    path('remove-container/<str:id_node>/<str:vmid>', views.removeContainer, name="remove-container"),

    # route start container
    path('start-container/<str:id_node>/<str:vmid>', views.startContainer, name="start-container"),
    # route stop container 
    path('stop-container/<str:id_node>/<str:vmid>', views.stopContainer, name="stop-container"),
    # route reboot container 
    path('reboot-container/<str:id_node>/<str:vmid>', views.rebootContainer, name="reboot-container"),

    # route add virtual_machine
    path('add-virtual-machine/<str:id_node>', views.addVirtualMachine, name="add-virtual-machine"), 

    # route remove virtual_machine
    path('remove-virtual-machine/<str:id_node>/<str:vmid>', views.removeVirtualMachine, name="remove-virtual-machine"),
    
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
    path('config/', views.config, name="config"),
    
    # route config_by_user
    path('config_by_user', views.config_by_user, name="config_by_user"),

    # package price
    path('package_price', views.package_price, name="package_price"),

    # route add package price
    path('add-package-price', views.addPackagePrice, name="add-package-price"),

    # route delete package price
    path('delete-package-price/<str:id_package_price>', views.deletePackagePrice, name="delete-package-price"), 

    # route edit package price
    path('edit-package-price/<str:id>', views.updatePackagePrice, name="edit-package-price"),


    # users all
    path('users_all', views.users_all, name="users_all"),

    # route add user client
    path('add-user-client', views.addUserClient, name="add-user-client"),

    # route delete user client
    path('delete-user-client/<str:id_user>', views.deleteUserClient, name="delete-user-client"), 

    # route active user client
    path('active-user-client/<str:id_user>', views.activeUserClient, name="active-user-client"),

    # route edit user client
    path('edit-user-client/<str:id_user>', views.updateUserClient, name="edit-user-client"),

    # order all
    path('order_all', views.order_all, name="order_all"),

    # order by user
    path('order_by_user/<str:id_user>', views.order_by_user, name="order_by_user"),

    # order execute
    path('order_execute', views.executeOrder, name="order_execute"),

    # delete order
    path('delete-order/<str:id_order>', views.deleteOrder, name="delete-order"), 

    # print invoice 
    path('print-invoice', views.printInvoice, name="print-invoice"),


]