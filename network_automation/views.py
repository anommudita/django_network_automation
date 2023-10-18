from django.shortcuts import render, redirect


# import data user untuk panel admin
from django.contrib.auth.models import User
# import model dari models.py
from .models import Server


# all form
# from network_automation.forms import ServerForm
from .forms import ServerForm


# import authenticate untuk login
from django.contrib.auth import authenticate , login, logout
# ketika nama  function sama dengan nama import maka buatkan aliasnya
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


from django.contrib.auth.decorators import login_required

# time
import time
import datetime


# get response json
from django.http import JsonResponse

import json

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

    # get data server
    server = Server.objects.get(id=1)
    username = server.username
    password = server.password
    ip_address = server.ip_address

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
    
def get_proxmox_paramiko():

    # get data server
    server = Server.objects.get(id=1)

    try:
        # setting datauser proxmox
        host = server.ip_address
        username = server.username
        password = server.password

        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        _stdin, _stdout,_stderr = client.exec_command("pvesh get cluster/resources --output-format json-pretty")

        
        data = json.loads(_stdout.read().decode())  # Mengubah hasil JSON menjadi struktur data Python
        client.close()
        return data  # Mengembalikan data sebagai struktur Python
    except Exception as e:
        print(e)
        return None


# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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

# halamn login
def login(request):
    

    # mengambil data dari form login
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password :
            messages.error(request, "Make sure username and password are valid")
            return redirect('login')

        try:
            # autentikasi user
            # mencari data user lalu dibandingkan dengan username dan password
            user = User.objects.get(username=username)
        except:
            # messages.error(request, 'User does not exist')
            pass

        # ketika berhasil login 
        # ini akan mengembalikan objek user cocok dengan kredesial ini atau none
        user = authenticate(request, username=username, password=password)

        # ketika user berhasil login
        if user is not None:
            # lagin berhasil
            # akan mencatat session database dan session di browser
            # ketika berhasil login akan diarahkan ke halaman home
            auth_login(request, user)
            return redirect('home')
        else:
            # login gagal
            # akan menampilkan pesan error
            messages.error(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)
            # return render(request, 'login.html')
    
def logout(request):

    # menghapus session di browser
    auth_logout(request)
    time.sleep(1.5)

    messages.success(request, "Successfully logged out")
    
    return redirect('login')

# halaman config
def config(request):
    # data by id
    server = Server.objects.get(id=1)

    # form dari form.py
    form = ServerForm(instance=server)

    # logic update data
    if request.method == "POST":
        form = ServerForm(request.POST, instance=server)
        if form.is_valid():
            form.save()
            # messages.success(request, "Server updated successfully")
            return redirect('home')
        else:
            # ketika form tidak valid atau kosong
            messages.error(request, "Make sure all fields are valid")
            return redirect('config')
        
    context = {
        'server' : server
    }
    return render(request, 'config.html', context)


# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
# # halaman utama
def home(request):
    proxmox = get_proxmox()

    if proxmox is not None:
        # Cluster Resources
        clusters = proxmox.cluster.resources.get()

        cpu_usage = 0
        mem_usage = 0
        disk_usage = 0
        maxcpu = 0
        maxmem = 0
        maxdisk = 0

        # Loop melalui data JSON
        for item in clusters:
            if "cpu" in item:
                # if "lxc" not in item["id"] and "qemu" not in item["id"]:
                    cpu_usage += item["cpu"]
            if "mem" in item:
                if "lxc" not in item["id"] and "qemu" not in item["id"]:
                    mem_usage += item["mem"]
            if "disk" in item:
                if "storage" in item["id"] and "lxc" not in item["id"] and "qemu" not in item["id"]:
                    disk_usage += item["disk"]
            if "maxcpu" in item:
                if "lxc" not in item["id"] and "qemu" not in item["id"]:
                    maxcpu += item["maxcpu"]
            if "maxmem" in item:
                if "lxc" not in item["id"] and "qemu" not in item["id"]:
                    maxmem += item["maxmem"]
            if "maxdisk" in item:
                if "storage" in item["id"] and "lxc" not in item["id"] and "qemu" not in item["id"]:
                    maxdisk += item["maxdisk"]

        # Anda dapat menyesuaikan operasi sesuai kebutuhan Anda.
        
        cpu_usage = round((cpu_usage / maxcpu) * 100 , 2)
        mem_usage = round(mem_usage / 1073741824 , 2)
        disk_usage = round(disk_usage / 1073741824 , 2)
        maxmem = round(maxmem / 1073741824 , 2)
        maxdisk = round(maxdisk / 1073741824 , 2)

        mem_percent = round ((mem_usage / maxmem) * 100, 2)
        disk_percent = round ((disk_usage / maxdisk) * 100, 2)

        # Pastikan data tersedia sebelum mencoba mengaksesnya


        # Log Resource
        log  = proxmox.cluster.log.get()


        # jumlah data user
        users = proxmox.access.users.get()
        count_user = len(users)

        context = {
            'title': 'Dashboard',
            'active_home': 'active',
            'cluster': clusters,  # Menggunakan indeks 0 karena data adalah list
            'cluster_cpu': cpu_usage,
            'cluster_mem': mem_usage,
            'cluster_disk': disk_usage,
            'cluster_maxcpu': maxcpu,
            'cluster_maxmem': maxmem,
            'cluster_maxdisk': maxdisk,
            'cluster_mempercent': mem_percent,
            'cluster_diskpercent': disk_percent,
        }
        return render(request, 'dashboard/home.html', context)
        
    else:
        # Redirect ke halaman eror jika koneksi gagal
        return redirect('error_connection')

# cluster resources di home
def cluster_resources(request):
    proxmox = get_proxmox()

    # Cluster Resources
    clusters = proxmox.cluster.resources.get()

    # Cluster Log
    # log = proxmox.cluster.log.get()

    if proxmox is not None:
        cpu_usage = 0
        mem_usage = 0
        disk_usage = 0
        maxcpu = 0
        maxmem = 0
        maxdisk = 0

        # Loop melalui data JSON
        for item in clusters:
            if "cpu" in item:
                # if "lxc" not in item["id"] and "qemu" not in item["id"]:
                    cpu_usage += item["cpu"]
            if "mem" in item:
                if "lxc" not in item["id"] and "qemu" not in item["id"]:
                    mem_usage += item["mem"]
            if "disk" in item:
                if "storage" in item["id"] and "lxc" not in item["id"] and "qemu" not in item["id"]:
                    disk_usage += item["disk"]
            if "maxcpu" in item:
                if "lxc" not in item["id"] and "qemu" not in item["id"]:
                    maxcpu += item["maxcpu"]
            if "maxmem" in item:
                if "lxc" not in item["id"] and "qemu" not in item["id"]:
                    maxmem += item["maxmem"]
            if "maxdisk" in item:
                if "storage" in item["id"] and "lxc" not in item["id"] and "qemu" not in item["id"]:
                    maxdisk += item["maxdisk"]

        # Anda dapat menyesuaikan operasi sesuai kebutuhan Anda.
        
        cpu_usage = round((cpu_usage / maxcpu) * 100 , 2)
        mem_usage = round(mem_usage / 1073741824 , 2)
        disk_usage = round(disk_usage / 1073741824 , 2)
        maxmem = round(maxmem / 1073741824 , 2)
        maxdisk = round(maxdisk / 1073741824 , 2)

        mem_percent = round ((mem_usage / maxmem) * 100, 2)
        disk_percent = round ((disk_usage / maxdisk) * 100, 2)


        # for item in log:
        #     # time
        #     date_from_proxmox = item['time']  # Get the date from Proxmox

        #     # You may need to parse the date_from_proxmox if it's in a specific format
        #     formatted_time = datetime.datetime.fromtimestamp(date_from_proxmox).strftime('%Y-%m-%d %H:%M:%S')

        #     pid = item['pid']
        #     node = item['node']
        #     user = item['user']
        #     msg = item['msg']
        #     tag = item['tag']

        # Pastikan data tersedia sebelum mencoba mengaksesnya

        data = {
            # resource
            'cluster_cpu': cpu_usage,
            'cluster_mem': mem_usage,
            'cluster_disk': disk_usage,
            'cluster_maxcpu': maxcpu,
            'cluster_maxmem': maxmem,
            'cluster_maxdisk': maxdisk,
            'cluster_mempercent': mem_percent,
            'cluster_diskpercent': disk_percent,

            # # log
            # 'log_time' : formatted_time,
            # 'log_pid' : pid,
            # 'log_node' : node,
            # 'log_user' : user,
            # 'log_msg' : msg,
            # 'log_tag' : tag,
        }
        return JsonResponse(data)
        
    else:
        # Redirect ke halaman eror jika koneksi gagal
        return redirect('error_connection')

def cluster_log(request):
    proxmox = get_proxmox()

    if proxmox is not None:
        # Cluster Resources
        log = proxmox.cluster.log.get()

        for item in log:
            # time
            date_from_proxmox = item['time']  # Get the date from Proxmox

            # You may need to parse the date_from_proxmox if it's in a specific format
            formatted_time = datetime.datetime.fromtimestamp(date_from_proxmox).strftime('%Y-%m-%d %H:%M:%S')

            pid = item['pid']
            node = item['node']
            user = item['user']
            msg = item['msg']
            tag = item['tag']

        # Pastikan data tersedia sebelum mencoba mengaksesnya

        data = {
            'cluster_log': log,
            'log_time' : formatted_time,
            'log_pid' : pid,
            'log_node' : node,
            'log_user' : user,
            'log_msg' : msg,
            'log_tag' : tag,
             
        }
        return JsonResponse(data)
        
    else:
        # Redirect ke halaman eror jika koneksi gagal
        return redirect('error_connection')


# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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
    


# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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
    
# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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

# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
#  delete user
def deleteUser(request, userid):

    proxmox = get_proxmox()
    proxmox.access.users(userid).delete()
    # user = User.objects.get(id=id)
    # user.delete()
    time.sleep(1.5)
    return redirect('user')

# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
#  halaman groups
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
        return redirect('error_connection')

# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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


# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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


# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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



# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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


# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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
        

# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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



# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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


# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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

    
# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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


# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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


# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
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



# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
# halaman node
def nodes(request):
    
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
            'title': 'Nodes',
            'active_node': 'active',
        }
        return render(request, 'node/node.html', context )
    else :
        return('error_connection')
    


# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
# halaman clusters
def clusters(request):
    
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
            'title': 'Clusters',
            'active_cluster': 'active',
        }
        return render(request, 'cluster/cluster.html', context )
    else :
        return('error_connection')


@login_required(login_url='login')
# halaman monitor
def monitors(request):
    
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
            'title': 'Monitors',
            'active_monitor': 'active',
        }
        return render(request, 'monitor/monitor.html', context )
    else :
        return('error_connection')
    

@login_required(login_url='login')
# halaman profile
def profile(request):
    
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
            'title': 'Monitors',
        }
        return render(request, 'settings/profile.html', context )
    else :
        return('error_connection')
    


@login_required(login_url='login')
# halaman settings
def settings(request):
    
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
            'title': 'Settings',
        }
        return render(request, 'settings/setting.html', context )
    else :
        return('error_connection')
    




