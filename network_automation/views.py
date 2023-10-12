from django.shortcuts import render, redirect

from  network_automation.models import User

# all form
from network_automation.forms import UserForm

# time
import time


# get response json
from django.http import JsonResponse

# import json

# import request dan jsonRespon untuk API promoxer
# import requests

# message flash django
from django.contrib import messages

# api proxmox
from proxmoxer import ProxmoxAPI

import paramiko

# Create your views here.



# function error conect to proxmoxer
def error_connection(request):
    return render(request, 'error.html')

def get_proxmox():
    try:
        # setting datauser proxmox
        proxmox =  ProxmoxAPI(
            '192.168.1.15',
            user='root@pam', 
            password='123123123', 
            verify_ssl=False)
        
        return proxmox
    except Exception as e:
        print(e)
        return None

# API Data AJAX
def data_api(request):
    action = request.GET.get('action')

    try:
        match action:
            case 'view_data_group':
                id = request.GET.get('id')
                proxmox = get_proxmox()
                group = proxmox.access.groups.get(id)
                response = {
                    'status': 'success',
                    'message': 'Data successfully retrieved',
                    'data': group
                }
                return JsonResponse(response)
            case 'view_data_user':
                id = request.GET.get('id')
                proxmox = get_proxmox()
                user = proxmox.access.users.get(id)
                response = {
                    'status': 'success',
                    'message': 'Data successfully retrieved',
                    'data': user
                }
                return JsonResponse(response)
            case 'view_data_role':
                roleid = request.GET.get('id')
                proxmox = get_proxmox()
                role = proxmox.access.roles.get(roleid)
                response = {
                    'status': 'success',
                    'message': 'Data successfully retrieved',
                    'data': role
                }
                return JsonResponse(response)
    except :
            return redirect('error_connection')


# halaman utama
def home(request):

    context = {
        'title': 'Dashboard',
        'active_home': 'active'
    }
    return render(request, 'dashboard/home.html', context )


#  halaman user
def  user(request):

    proxmox = get_proxmox()

    if proxmox is not None:
        # user
        users = proxmox.access.users.get()

        # groups
        groups = proxmox.access.groups.get()
        
        context = {
            'title': 'Users',
            'active_user': 'active',
            'users': users,
            'groups': groups,
        }
        return render(request, 'user/user.html', context )
    else:
        # Redirect ke halaman eror jika koneksi gagal
        return redirect('error_connection')

# add user
def  addUser(request):
    # connect to proxmox
    proxmox = get_proxmox()

    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        group = request.POST.get('group')

        if not firstname or not lastname or not email or not username or not password :
            messages.error(request, "Make sure all fields are valid")
            return redirect('user')
        
        try:
            proxmox.access.users.create(firstname=firstname, lastname=lastname, email=email, userid=username + '@pve', password=password, groups=group)
            messages.success(request, "User added successfully")
            return redirect('user')
        except Exception as e:
            messages.error(request, f"Error adding user : {str(e)}")
            return redirect('user')
    

def  updateUser(request, id):

    proxmox = get_proxmox()

    if request.method == "POST":
        firstname = request.POST.get('edit_firstname')
        lastname = request.POST.get('edit_lastname')
        email = request.POST.get('edit_email')
        password1 = request.POST.get('edit_password')
        group = request.POST.get('edit_group')
        userid = id

        if not firstname or not lastname or not email :
            messages.error(request, "Make sure all fields are valid")
            return redirect('user')
        try:
            proxmox.access.users(userid).put(email=email, firstname=firstname, lastname=lastname, groups=group)

            # jika password diisi maka ganti password lama dengan password baru
            if password1 :
                proxmox.access.password.put(userid=userid, password=password1)

            messages.success(request, "User saved successfully")
            return redirect('user')
        except Exception as e:
            messages.error(request, f"Error saved user: {str(e)}")
            return redirect('user')      


#  delete user
def deleteUser(request, userid):

    proxmox = get_proxmox()
    proxmox.access.users(userid).delete()
    # user = User.objects.get(id=id)
    # user.delete()
    time.sleep(1.5)
    return redirect('user')

#  halaman guru
def  groups(request):

    proxmox = get_proxmox()
    if proxmox is not None :
        groups = proxmox.access.groups.get()
    
        context = {
            'title': 'Groups',
            'active_user': 'active',
            'groups': groups,
        }
        return render(request, 'user/groups.html', context )
    else:
        return redirect(error_connection)

# add groups
def  addGroup(request):
    # connect to proxmox
    proxmox = get_proxmox()

    if request.method == "POST":
        name = request.POST.get('name')
        comment = request.POST.get('comment')

        if not name or not comment:
            messages.error(request, "Make sure all fields are valid")
            return redirect('groups')
        
        try:
            proxmox.access.groups.create(groupid=name, comment=comment)
            messages.success(request, "Group added successfully")
            return redirect('groups')
        except Exception as e:
            messages.error(request, f"Error adding group: {str(e)}")
            return redirect('groups')


# updateGroup
def  updateGroup(request, groupid):
    
    proxmox = get_proxmox()

    if request.method == "POST":
        comment = request.POST.get('edit_comment')

        if comment == "None":
            messages.error(request, "Make sure all fields are valid")
            return redirect('groups')
        
        try:
            proxmox.access.groups(groupid).put(comment=comment)
            messages.success(request, "Group saved successfully")
            return redirect('groups')
        except Exception as e:
            messages.error(request, f"Error saved group: {str(e)}")
            return redirect('groups')      


# delete group
def deleteGroup(request, groupid):
    # connect to proxmox
    proxmox = get_proxmox()
    try :
        proxmox.access.groups(groupid).delete()
        time.sleep(1.5)
        return redirect('groups')
    except Exception as e:
        messages.error(request, f"Error deleting group: {str(e)}")
        return redirect('groups')


#  halaman permissions
def  permissions(request):

    proxmox = get_proxmox()

    if proxmox is not None :
        # acl
        permissions = proxmox.access.acl.get()

        # path
        get_permissins = proxmox.access.permissions.get()
        path_list = []
        for key in get_permissins:
            path_list.append(key)

        path = path_list

        # roles
        roles = proxmox.access.roles.get()

        # group
        groups = proxmox.access.groups.get()

        # users
        users = proxmox.access.users.get() 

        context = {
        'title': 'Permissions',
        'active_user': 'active',
        'permissions': permissions,
        'roles': roles,
        'path': path,
        'groups': groups,
        'users': users,
        }
        return render(request, 'user/permissions.html', context )
    else:
        return redirect(error_connection)

# add permissions group
def addPermissionGroup(request):
    # connect to proxmox
    proxmox = get_proxmox()

    if request.method == "POST":
        roles = request.POST.get('role')
        group = request.POST.get('group')
        path = request.POST.get('path')
        propagate = request.POST.get('propagateGroup')

        if propagate:
            propagate = 1
        else:
            propagate = 0

        if not roles or not group or not path:
            messages.error(request, "Make sure all fields are valid")
            return redirect('permissions')
        try:
            proxmox.access.acl.put(path=path, roles=roles, groups=group, propagate=propagate)
            messages.success(request, "Permissions Group added successfully")
            return redirect('permissions')
        except Exception as e:
            messages.error(request, f"Error adding permissions group: {str(e)}")
            return redirect('permissions')
        
# add permissions User
def addPermissionUser(request):
    # connect to proxmox
    proxmox = get_proxmox()

    if request.method == "POST":
        roles = request.POST.get('role2')
        user = request.POST.get('user')
        path = request.POST.get('path2')
        propagate = request.POST.get('propagateUser')

        if propagate:
            propagate = 1
        else:
            propagate = 0

        if not roles or not user or not path:
            messages.error(request, "Make sure all fields are valid")
            return redirect('permissions')
        try:
            proxmox.access.acl.put(path=path, roles=roles, users=user, propagate=propagate)
            messages.success(request, "Permissions User added successfully")
            return redirect('permissions')
        except Exception as e:
            messages.error(request, f"Error adding permissions user: {str(e)}")
            return redirect('permissions')


# add permissions API
def addPermissionAPI(request):
    # connect to proxmox
    proxmox = get_proxmox()

    if request.method == "POST":
        roles = request.POST.get('role3')
        API = request.POST.get('API')
        path = request.POST.get('path3')
        propagate = request.POST.get('propagateAPI')

        if propagate:
            propagate = 1
        else:
            propagate = 0

        if not roles or not API or not path:
            messages.error(request, "Make sure all fields are valid")
            return redirect('permissions')
        try:
            proxmox.access.acl.put(path=path, roles=roles, tokens=API, propagate=propagate)
            messages.success(request, "Permissions API Token added successfully")
            return redirect('permissions')
        except Exception as e:
            messages.error(request, f"Error adding permissions API token : {str(e)}")
            return redirect('permissions')


# delete permission
def deletePermissions(request, path, roles, type, ugid):

    # connect to proxmox
    proxmox = get_proxmox()
    try :

        if type == "group":
            proxmox.access.acl.put(path=path, roles=roles, groups=ugid, delete=1)
        elif type == "user":
            proxmox.access.acl.put(path=path, roles=roles, users=ugid, delete=1)
        elif type == "token":
            proxmox.access.acl.put(path=path, roles=roles, tokens=ugid, delete=1)

        time.sleep(1.5)
        return redirect('permissions')
    except Exception as e:
        messages.error(request, f"Error deleting permissions : {str(e)}")
        return redirect('permissions')

#  roles
def roles(request):

    proxmox = get_proxmox()

    if proxmox is not None :
        roles = proxmox.access.roles.get()

        privs = []

        # menampilkan data select option dari data list roles
        for item in roles:
            if item['roleid'] == 'Administrator':
                privs_string = item['privs']
                privs = [priv.strip() for priv in privs_string.split(',')]  # Memisahkan privs dengan koma
        
        context = {
            'title': 'Roles',
            'active_user': 'active',
            'roles': roles,
            'privs': privs,
        }
        return render(request, 'user/roles.html', context )
    else :
        return('error_connection')

    


# add roles
def addRole(request):
# connect to proxmox
    proxmox = get_proxmox()

    if request.method == "POST":
        name = request.POST.get('name')
        privileges = request.POST.getlist('privileges')

        if not name or not privileges :
            messages.error(request, "Make sure all fields are valid")
            return redirect('roles')
        
        # Menggabungkan daftar privileges menjadi satu string yang dipisahkan dengan koma
        privileges_str = ','.join(privileges)

        try:
            proxmox.access.roles.create(roleid=name, privs=privileges_str)
            messages.success(request, "Role added successfully")
            return redirect('roles')
        except Exception as e:
            messages.error(request, f"Error adding permissions roles : {str(e)}")
            return redirect('roles')

# update roles 
def  updateRole(request, roleid):
    
    proxmox = get_proxmox()

    if request.method == "POST":
        privileges = request.POST.getlist('edit_privileges')

        if not privileges :
            messages.error(request, "Make sure all fields are valid")
            return redirect('roles')
        
        # Menggabungkan daftar privileges menjadi satu string yang dipisahkan dengan koma
        privileges_str = ','.join(privileges)

        try:
            proxmox.access.roles(roleid).put(privs=privileges_str)
            messages.success(request, "Role updated successfully")
            return redirect('roles')
        except Exception as e:
            messages.error(request, f"Error updated permissions roles : {str(e)}")
            return redirect('roles')  
        
# delete role
def deleteRole(request, roleid):

    # connect to proxmox
    proxmox = get_proxmox()
    try :
        proxmox.access.roles(roleid).delete()
        time.sleep(1.5)
        return redirect('roles')
    except Exception as e:
        messages.error(request, f"Error deleting roles : {str(e)}")
        return redirect('roles')


