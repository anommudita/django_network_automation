from django.shortcuts import render, redirect


# import data user untuk panel admin
from django.contrib.auth.models import User
# import model dari models.py
from .models import Server, UserProfile

# all form
# from network_automation.forms import ServerForm
from .forms import ServerForm, UpdateProfileAvatar, UpdateProfile, UpdateUserProfile


from django.contrib.auth.hashers import make_password  # Import fungsi make_password


# import authenticate untuk login
from django.contrib.auth import authenticate , login, logout
# ketika nama  function sama dengan nama import maka buatkan aliasnya
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


from django.contrib.auth.decorators import login_required

# time
import time
import datetime

# import enum
from enum import Enum


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
            ip_address,
            user=username + '@pam', 
            password=password, 
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
            case 'view_data_cluster_resources':
                proxmox = get_proxmox()

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

                response = {
                    # resource
                    'cluster_cpu': cpu_usage,
                    'cluster_mem': mem_usage,
                    'cluster_disk': disk_usage,
                    'cluster_maxcpu': maxcpu,
                    'cluster_maxmem': maxmem,
                    'cluster_maxdisk': maxdisk,
                    'cluster_mempercent': mem_percent,
                    'cluster_diskpercent': disk_percent,

                }
                return JsonResponse(response)
            case 'view_data_cluster_log':
                proxmox = get_proxmox()
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

                response = {
                    'status': 'success',
                    'message': 'Data successfully retrieved',
                    'cluster_log': log,
                    'log_time' : formatted_time,
                    'log_pid' : pid,
                    'log_node' : node,
                    'log_user' : user,
                    'log_msg' : msg,
                    'log_tag' : tag,
                }
                return JsonResponse(response)
            case 'view_data_nodes_resources':
                proxmox = get_proxmox()
                nodes = proxmox.nodes.get()
                node_data = []

                for node in nodes:
                    if node.get('status') == 'online':
                        id = node.get('id')
                        cpu_usage = node.get('cpu')
                        mem_usage = node.get('mem')
                        disk_usage = node.get('disk')
                        maxcpu = node.get('maxcpu')
                        maxmem = node.get('maxmem')
                        maxdisk = node.get('maxdisk')
                        uptime = node.get('uptime')

                        # Anda dapat menyesuaikan operasi sesuai kebutuhan Anda.
                        cpu_usage = round((cpu_usage / maxcpu) * 100, 2)
                        mem_usage = round(mem_usage / 1073741824, 2)
                        disk_usage = round(disk_usage / 1073741824, 2)
                        maxmem = round(maxmem / 1073741824, 2)
                        maxdisk = round(maxdisk / 1073741824, 2)
                        mem_percent = round((mem_usage / maxmem) * 100, 2)
                        disk_percent = round((disk_usage / maxdisk) * 100, 2)
                        hours, remainder = divmod(uptime, 3600)
                        minute, second = divmod(remainder, 60)

                        node_data.append({
                            'node_id': node.get('id'),
                            'node_name': node.get('node'),
                            'node_status': node.get('status'),
                            'nodes_cpu': cpu_usage,
                            'nodes_mem': mem_usage,
                            'nodes_disk': disk_usage,
                            'nodes_maxcpu': maxcpu,
                            'nodes_maxmem': maxmem,
                            'nodes_maxdisk': maxdisk,
                            'nodes_mempercent': mem_percent,
                            'nodes_diskpercent': disk_percent,
                            'nodes_hours': hours,
                            'nodes_minutes': minute,
                            'nodes_second': second,
                        })
                    
                    else:
                        node_data.append({
                            'node_id': node.get('id'),
                            'node_name': node.get('node'),
                            'node_status': node.get('status'),
                        })
                # Buat JSON response
                response = {
                    'node_data': node_data,
                }
                
                return JsonResponse(response)
            case 'view_data_ct_resources':
                id_node = request.GET.get('id_node')  # Mengambil ID node dari permintaan GET

                if id_node is not None:
                    proxmox = get_proxmox()
                    containers = proxmox.nodes(id_node).lxc.get()
                    container_data = []

                    for container in containers:
                        name = container.get('name')
                        vmid = container.get('vmid')
                        cpu_usage = container.get('cpu')
                        mem_usage = container.get('mem')
                        disk_usage = container.get('disk')
                        maxcpu = container.get('cpus')
                        maxmem = container.get('maxmem')
                        maxdisk = container.get('maxdisk')
                        uptime = container.get('uptime')

                        # Anda dapat menyesuaikan operasi sesuai kebutuhan Anda.
                        cpu_usage = round((cpu_usage / maxcpu) * 100, 2)
                        mem_usage = round(mem_usage / 1073741824, 2)
                        disk_usage = round(disk_usage / 1073741824, 2)
                        maxmem = round(maxmem / 1073741824, 2)
                        maxdisk = round(maxdisk / 1073741824, 2)
                        mem_percent = round((mem_usage / maxmem) * 100, 2)
                        disk_percent = round((disk_usage / maxdisk) * 100, 2)
                        hours, remainder = divmod(uptime, 3600)
                        minute, second = divmod(remainder, 60)

                        container_data.append({
                            'container_status': container.get('status'),
                            'container_name': name,
                            'container_vmid': vmid,
                            'container_cpu': cpu_usage,
                            'container_mem': mem_usage,
                            'container_disk': disk_usage,
                            'container_maxcpu': maxcpu,
                            'container_maxmem': maxmem,
                            'container_maxdisk': maxdisk,
                            'container_mempercent': mem_percent,
                            'container_diskpercent': disk_percent,
                            'container_hours': hours,
                            'container_minutes': minute,
                            'container_seconds': second,
                        })

                    # Buat JSON response
                    response = {
                        'container_data': container_data,
                    }
                    
                    return JsonResponse(response)
                else:
                    # Tanggapan jika id_node tidak diberikan
                    return JsonResponse({'error': 'ID node tidak diberikan'})
                
            case 'view_data_vm_resources':
                id_node = request.GET.get('id_node')  # Mengambil ID node dari permintaan GET

                if id_node is not None:
                    proxmox = get_proxmox()
                    vms = proxmox.nodes(id_node).qemu.get()
                    vm_data = []

                    for vm in vms:
                        name = vm.get('name')
                        vmid = vm.get('vmid')
                        cpu_usage = vm.get('cpu')
                        mem_usage = vm.get('mem')
                        disk_usage = vm.get('disk')
                        maxcpu = vm.get('cpus')
                        maxmem = vm.get('maxmem')
                        maxdisk = vm.get('maxdisk')
                        uptime = vm.get('uptime')

                        # Anda dapat menyesuaikan operasi sesuai kebutuhan Anda.
                        cpu_usage = round((cpu_usage / maxcpu) * 100, 2)
                        mem_usage = round(mem_usage / 1073741824, 2)
                        disk_usage = round(disk_usage / 1073741824, 2)
                        maxmem = round(maxmem / 1073741824, 2)
                        maxdisk = round(maxdisk / 1073741824, 2)
                        mem_percent = round((mem_usage / maxmem) * 100, 2)
                        disk_percent = round((disk_usage / maxdisk) * 100, 2)
                        hours, remainder = divmod(uptime, 3600)
                        minute, second = divmod(remainder, 60)

                        vm_data.append({
                            'vm_status': vm.get('status'),
                            'vm_name': name,
                            'vm_vmid': vmid,
                            'vm_cpu': cpu_usage,
                            'vm_mem': mem_usage,
                            'vm_disk': disk_usage,
                            'vm_maxcpu': maxcpu,
                            'vm_maxmem': maxmem,
                            'vm_maxdisk': maxdisk,
                            'vm_mempercent': mem_percent,
                            'vm_diskpercent': disk_percent,
                            'vm_hours': hours,
                            'vm_minutes': minute,
                            'vm_seconds': second,
                        })

                    # Buat JSON response
                    response = {
                        'vm_data': vm_data,
                    }
                    
                    return JsonResponse(response)
                else:
                    # Tanggapan jika id_node tidak diberikan
                    return JsonResponse({'error': 'ID node tidak diberikan'})
            case 'view_data_network':
                iface = request.GET.get('iface')
                type = request.GET.get('type')
                node = request.GET.get('node')
                proxmox = get_proxmox()
                network = proxmox.nodes(node).network(iface=iface, type=type).get()
                response = {
                    'status': 'success',
                    'message': 'Data successfully retrieved',
                    'data': network
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
            messages.success(request, "Server updated successfully")
            return redirect('home')
        else:
            # ketika form tidak valid atau kosong
            messages.error(request, "Make sure all fields are valid")
            return redirect('config')
        
    context = {
        'server' : server
    }
    return render(request, 'config.html', context)


# halaman config by user
def config_by_user(request):
    # data by id
    server = Server.objects.get(id=1)

    # form dari form.py
    form = ServerForm(instance=server)

    # logic update data
    if request.method == "POST":
        form = ServerForm(request.POST, instance=server)
        if form.is_valid():
            form.save()
            messages.success(request, "Server updated successfully")
            return redirect('home')
        else:
            # ketika form tidak valid atau kosong
            messages.error(request, "Make sure all fields are valid")
            return redirect('settings')
    


# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
# # halaman utama
def home(request):
    proxmox = get_proxmox()

    if proxmox is not None:

        # # jumlah data user
        users = proxmox.access.users.get()
        count_user = len(users)

        cluster = proxmox.cluster.status.get()
        cluster_status = cluster[0]
        
        if cluster_status['type'] == 'cluster':
            cluster_name = cluster_status['name']
        else:
            cluster_name = '-'

        if 'nodes' in cluster_status:
            node = cluster_status['nodes']
        else:
            node = cluster_status['name']
        
        node_online = 0

        for item in cluster:
            if 'online' in item:
                node_online += item['online']

        context = {
            'title': 'Dashboard',
            'active_home': 'active',
            'count_user': count_user,
            'cluster_name': cluster_name,
            'node': node,
            'cluster_online': node_online,
        }
        return render(request, 'dashboard/home.html', context)
        
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
        nodes = proxmox.nodes.get()

        
        context = {
            'title': 'Nodes',
            'active_node': 'active',
            'nodes': nodes,
        }
        return render(request, 'node/node.html', context )
    else :
        return('error_connection')
    

# netmask to prefix || netmask to desimal
def netmask_to_prefix(netmask):
    netmask = int(netmask)  # Mengonversi ke integer jika belum
    # Membuat daftar 8 bit yang mewakili masing-masing bagian dari netmask
    binary_netmask = "1" * netmask + "0" * (32 - netmask)
    
    # Memisahkan daftar 8 bit menjadi empat bagian dan mengonversinya ke desimal
    parts = [int(binary_netmask[i:i+8], 2) for i in range(0, 32, 8)]
    
    # Menggabungkan empat bagian dalam notasi netmask
    netmask_str = ".".join(map(str, parts))
    
    return netmask_str



# network node
@login_required(login_url='login')
def networkNode(request, id_node):
    proxmox = get_proxmox()
    if proxmox is not None:

        # id node
        id_node = id_node


        # get network by id 
        # pvesh get /nodes/{node}/network/{iface}
        # network1 = proxmox.nodes(id_node).network('bond1').get()

        # get_data = {
        #                 "iface" : name,
        #                 "type" : "bridge",
        # }

        # network1 = proxmox.nodes(id_node).network.get(**get_data)

        # get network
        network = proxmox.nodes(id_node).network.get()
        
        context = {
            'title': 'Network',
            'active_node': 'active',
            'network': network,
            'id_node': id_node,
        }
        return render(request, 'node/network.html', context )
    else:
        # Redirect ke halaman eror jika koneksi gagal
        return redirect('error_connection')

# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
# delete group
def NetworkApply(request, id_node):
    # connect to proxmox
    proxmox = get_proxmox()
    try :
        proxmox.nodes(id_node).network.put()
        time.sleep(1.5)
        messages.success(request, "Apply Configuration successfully")
        return redirect('node-network', id_node)
    except Exception as e:
        messages.error(request, f"Error apply configuration : {str(e)}")
        return redirect('node-network', id_node)

# network node
@login_required(login_url='login')
def addLinuxBridge(request, id_node):
    proxmox = get_proxmox()
    if proxmox is not None:
        # # id node                                                 
        id_node = id_node
        if request.method == "POST":
            name = request.POST.get('name')
            ipv4 = request.POST.get('ipv4')
            netmask = request.POST.get('netmask')
            gateway = request.POST.get('gateway_cidr4')
            bridgePort = request.POST.get('bridgePort')

            # cidr = ipv4 + '/' + netmask
            # cidr6 = ipv6 + '/' + netmask6

            # ketika vlan aware di centang
            if 'vlanAware' in request.POST:
                vlan_Aware = 1
            else:
                vlan_Aware = 0

            # messages.success(request, "Mode " + type) 
            
            # ketika autostar di centang atau default-nya 1
            if 'autoStart' in request.POST:
                autostart = 1
            else:
                autostart = 0

            if not name or not ipv4 or not netmask :
                messages.error(request, "Make sure all fields are valid")
                return redirect('node-network', id_node)
            
            # ketika ipv4 di isi 
            if 'ipv4' in request.POST or 'netmask' in request.POST :
                desimal_to_netmask = netmask_to_prefix(netmask)


                # kondisi ketika gateway di isi 
                if gateway != '':
                    post_data = {
                        "iface" : name,
                        "type" : "bridge",
                        "address":ipv4,
                        "gateway" : gateway,
                        "netmask" : desimal_to_netmask,
                        "autostart"  : autostart,
                        "bridge_ports" : bridgePort,
                        "bridge_vlan_aware" : vlan_Aware,
                    }

                # kondisi ketika gateway tidak di isi atau sama dengan null
                if gateway == '':
                    post_data = {
                        "iface" : name,
                        "type" : "bridge",
                        "address":ipv4,
                        # "gateway" : gateway,
                        "netmask" : desimal_to_netmask,
                        "autostart"  : autostart,
                        "bridge_ports" : bridgePort,
                        "bridge_vlan_aware" : vlan_Aware,
                    }

                try:
                    proxmox.nodes(id_node).network.post(**post_data)
                    messages.success(request, "Network Linux Bridge added successfully")
                    return redirect('node-network', id_node)
                except Exception as e:
                    messages.error(request, f"Error adding network : {str(e)}")
                    return redirect('node-network', id_node)
    else:
        # Redirect ke halaman eror jika koneksi gagal
        return redirect('error_connection')
    

# network mode linux bond
@login_required(login_url='login')
def addLinuxBond(request, id_node):
    proxmox = get_proxmox()
    if proxmox is not None:
        # # id node                                                 
        id_node = id_node
        if request.method == "POST":
            name = request.POST.get('name_bond')
            ipv4 = request.POST.get('ipv4_bond')
            netmask = request.POST.get('netmask_bond')
            gateway = request.POST.get('gateway_bond')
            slaves = request.POST.get('slave_bond')
            mode = request.POST.get('mode_bond')

            # bond_primary dan hash_policy
            bond_primary = request.POST.get('bond_primary')
            hash_policy = request.POST.get('hash_policy')
            
            # ketika autostar di centang atau default-nya 1
            if 'autoStartBond' in request.POST:
                autostart = 1
            else:
                autostart = 0

            if not name :
                messages.error(request, "Make sure all fields are valid")
                return redirect('node-network', id_node)
            
            # ketika mode ballance-rr atau balance-alb atau balance-tlb
            if mode == 'balance-rr' or mode == 'balance-alb' or mode == 'balance-tlb':
                # ketika ipv4 di isi
                if ipv4 != '' and netmask != '':
                    desimal_to_netmask = netmask_to_prefix(netmask)
                    post_data = {
                    "iface" : name,
                    "type" : "bond",
                    "slaves" : slaves,
                    "bond_mode" : mode,
                    "address":ipv4,
                    "netmask" : desimal_to_netmask,
                    "autostart"  : autostart,
                    }

                # ketika ada gateway
                if gateway !='':
                    desimal_to_netmask = netmask_to_prefix(netmask)
                    post_data = {
                    "iface" : name,
                    "type" : "bond",
                    "slaves" : slaves,
                    "bond_mode" : mode,
                    "address":ipv4,
                    "netmask" : desimal_to_netmask,
                    "gateway" : gateway,
                    "autostart"  : autostart,
                    }
                # ketika gateway kosong dan ipv4 kosong dan netmask kosong
                if gateway == '' and ipv4 == '' and netmask == '':
                    post_data = {
                        "iface" : name,
                        "type" : "bond",
                        "slaves" : slaves,
                        "bond_mode" : mode,
                        "autostart"  : autostart,
                    }

            # ketika mode active-backup
            if mode == 'active-backup':
                # ketika ipv4 di isi
                if ipv4 != '' and netmask != '':
                    desimal_to_netmask = netmask_to_prefix(netmask)
                    post_data = {
                    "iface" : name,
                    "type" : "bond",
                    "slaves" : slaves,
                    "bond_mode" : mode,
                    "bond-primary" : bond_primary,
                    "address":ipv4,
                    "netmask" : desimal_to_netmask,
                    "autostart"  : autostart,
                    }

                # ketika ada gateway
                if gateway !='':
                    desimal_to_netmask = netmask_to_prefix(netmask)
                    post_data = {
                    "iface" : name,
                    "type" : "bond",
                    "slaves" : slaves,
                    "bond-primary" : bond_primary,
                    "bond_mode" : mode,
                    "address":ipv4,
                    "netmask" : desimal_to_netmask,
                    "gateway" : gateway,
                    "autostart"  : autostart,
                    }
                # ketika gateway kosong dan ipv4 kosong dan netmask kosong
                if gateway == '' and ipv4 == '' and netmask == '':
                    post_data = {
                        "iface" : name,
                        "type" : "bond",
                        "slaves" : slaves,
                        "bond-primary" : bond_primary,
                        "bond_mode" : mode,
                        "autostart"  : autostart,
                    }

            # ketika mode balance-xor
            if mode == 'balance-xor':
                # ketika ipv4 di isi
                if ipv4 != '' and netmask != '':
                    desimal_to_netmask = netmask_to_prefix(netmask)
                    post_data = {
                    "iface" : name,
                    "type" : "bond",
                    "slaves" : slaves,
                    "bond_mode" : mode,
                    "bond_xmit_hash_policy" : hash_policy,
                    "address":ipv4,
                    "netmask" : desimal_to_netmask,
                    "autostart"  : autostart,
                    }

                # ketika ada gateway
                if gateway !='':
                    desimal_to_netmask = netmask_to_prefix(netmask)
                    post_data = {
                    "iface" : name,
                    "type" : "bond",
                    "slaves" : slaves,
                    "bond_mode" : mode,
                    "bond_xmit_hash_policy" : hash_policy,
                    "address":ipv4,
                    "netmask" : desimal_to_netmask,
                    "gateway" : gateway,
                    "autostart"  : autostart,
                    }
                # ketika gateway kosong dan ipv4 kosong dan netmask kosong
                if gateway == '' and ipv4 == '' and netmask == '':
                    post_data = {
                        "iface" : name,
                        "type" : "bond",
                        "slaves" : slaves,
                        "bond_mode" : mode,
                        "bond_xmit_hash_policy" : hash_policy,
                        "autostart"  : autostart,
                    }

            # ketika mode broadcast
            if mode == 'broadcast':
                # ketika ipv4 di isi
                if ipv4 != '' and netmask != '':
                    desimal_to_netmask = netmask_to_prefix(netmask)
                    post_data = {
                    "iface" : name,
                    "type" : "bond",
                    "slaves" : slaves,
                    "bond_mode" : mode,
                    "address":ipv4,
                    "netmask" : desimal_to_netmask,
                    "autostart"  : autostart,
                    }

                # ketika ada gateway
                if gateway !='':
                    desimal_to_netmask = netmask_to_prefix(netmask)
                    post_data = {
                    "iface" : name,
                    "type" : "bond",
                    "slaves" : slaves,
                    "bond_mode" : mode,
                    "address":ipv4,
                    "netmask" : desimal_to_netmask,
                    "gateway" : gateway,
                    "autostart"  : autostart,
                    }
                # ketika gateway kosong dan ipv4 kosong dan netmask kosong
                if gateway == '' and ipv4 == '' and netmask == '':
                    post_data = {
                        "iface" : name,
                        "type" : "bond",
                        "slaves" : slaves,
                        "bond_mode" : mode,
                        "autostart"  : autostart,
                    }

            # ketika mode 802.3ad
            if mode == '802.3ad':
                # ketika ipv4 di isi
                if ipv4 != '' and netmask != '':
                    desimal_to_netmask = netmask_to_prefix(netmask)
                    post_data = {
                    "iface" : name,
                    "type" : "bond",
                    "slaves" : slaves,
                    "bond_mode" : mode,
                    "bond_xmit_hash_policy" : hash_policy,
                    "address":ipv4,
                    "netmask" : desimal_to_netmask,
                    "autostart"  : autostart,
                    }

                # ketika ada gateway
                if gateway !='':
                    desimal_to_netmask = netmask_to_prefix(netmask)
                    post_data = {
                    "iface" : name,
                    "type" : "bond",
                    "slaves" : slaves,
                    "bond_mode" : mode,
                    "bond_xmit_hash_policy" : hash_policy,
                    "address":ipv4,
                    "netmask" : desimal_to_netmask,
                    "gateway" : gateway,
                    "autostart"  : autostart,
                    }
                # ketika gateway kosong dan ipv4 kosong dan netmask kosong
                if gateway == '' and ipv4 == '' and netmask == '':
                    post_data = {
                        "iface" : name,
                        "type" : "bond",
                        "slaves" : slaves,
                        "bond_mode" : mode,
                        "bond_xmit_hash_policy" : hash_policy,
                        "autostart"  : autostart,
                    }

            try:
                proxmox.nodes(id_node).network.post(**post_data)
                messages.success(request, "Network Linux Bond added successfully")
                return redirect('node-network', id_node)
            except Exception as e:
                messages.error(request, f"Error adding network : {str(e)}")
                return redirect('node-network', id_node)
    else:
        # Redirect ke halaman eror jika koneksi gagal
        return redirect('error_connection')
    

# network mode linux vlan
@login_required(login_url='login')
def addLinuxVlan(request, id_node):
    proxmox = get_proxmox()
    if proxmox is not None:
        # # id node                                                 
        id_node = id_node
        if request.method == "POST":
            name = request.POST.get('name_vlan')
            ipv4 = request.POST.get('ipv4_vlan')
            netmask = request.POST.get('netmask_vlan')
            gateway = request.POST.get('gateway_vlan')


            # vlan
            vlan_raw_device = request.POST.get('vlan_raw_device')
            vlan_tag = request.POST.get('vlan_tag')
            
            # ketika autostar di centang atau default-nya 1
            if 'autoStartVlan' in request.POST:
                autostart = 1
            else:
                autostart = 0

            if not name :
                messages.error(request, "Make sure all fields are valid")
                return redirect('node-network', id_node)
            
            # ketika mode ballance-rr atau balance-alb atau balance-tlb
            if name :
                # ketika ipv4 di isi
                if ipv4 != '' and netmask != '':
                    desimal_to_netmask = netmask_to_prefix(netmask)
                    post_data = {
                    "iface" : name,
                    "type" : "vlan",
                    "vlan-id" : vlan_tag,
                    "vlan-raw-device" : vlan_raw_device,
                    "address":ipv4,
                    "netmask" : desimal_to_netmask,
                    "autostart"  : autostart,
                    }

                # ketika ada gateway
                if gateway !='':
                    desimal_to_netmask = netmask_to_prefix(netmask)
                    post_data = {
                    "iface" : name,
                    "type" : "vlan",
                    "vlan-id" : vlan_tag,
                    "vlan-raw-device" : vlan_raw_device,
                    "address":ipv4,
                    "netmask" : desimal_to_netmask,
                    "gateway" : gateway,
                    "autostart"  : autostart,
                    }
                    
                # ketika gateway kosong dan ipv4 kosong dan netmask kosong
                if gateway == '' and ipv4 == '' and netmask == '':
                    post_data = {
                        "iface" : name,
                        "type" : "vlan",
                        "vlan-id" : vlan_tag,
                        "vlan-raw-device" : vlan_raw_device,
                        "autostart"  : autostart,
                    }
            try:
                proxmox.nodes(id_node).network.post(**post_data)
                messages.success(request, "Network Linux Bond added successfully")
                return redirect('node-network', id_node)
            except Exception as e:
                messages.error(request, f"Error adding network : {str(e)}")
                return redirect('node-network', id_node)
    else:
        # Redirect ke halaman eror jika koneksi gagal
        return redirect('error_connection')
    



# wajib login untuk mengakses halaman ini
@login_required(login_url='login')
# delete group
def deleteNetwork(request, iface, id_node):
    # connect to proxmox
    proxmox = get_proxmox()
    try :
        proxmox.nodes(id_node).network(iface).delete()
        time.sleep(1.5)
        messages.success(request, "Network deleted successfully")
        return redirect('node-network', id_node)
    except Exception as e:
        messages.error(request, f"Error deleting iface: {str(e)}")
        return redirect('node-network', id_node)



@login_required(login_url='login')
# halaman detail_node
def detail_node(request, id_node):
    
    proxmox = get_proxmox()

    if proxmox is not None :

        # id node
        id_node = id_node

        # data resource pool
        resource_pool = proxmox.pools.get()

        # template
        templates = proxmox.nodes(id_node).storage('local').content.get()

        # ISO Container Templated
        iso_container = []

        # container
        for item in templates:
            if item['format'] == 'tzst' or item['format'] == 'tar.gz':
                # volid :
                volid = item['volid']
                # format :
                format = item['format']
                # size :
                size = round(item['size'] / 1048576, 2)

                
                # disk_usage = round(disk_usage / 1073741824, 2)
                iso_container.append({
                    'volid': volid,
                    'format': format,
                    'size': size,
                })

        # ISO Virtual Machine
        iso_virtual_machine = []

        for item in templates:
            if item['format'] == 'iso':
                # volid :
                volid = item['volid']
                # format :
                format = item['format']
                # size :
                size = round(item['size'] / 1048576, 2)

                
                # disk_usage = round(disk_usage / 1073741824, 2)
                iso_virtual_machine.append({
                    'volid': volid,
                    'format': format,
                    'size': size,
                })


        # get network proxmox
        network_proxmox = proxmox.nodes(id_node).network.get()

        # get network berdasarkan type bridge
        network = []

        for item in network_proxmox:
            if item['type'] == 'bridge':
                # iface :
                iface = item['iface']
                # type :
                type = item['type']
                
                network.append({
                    'iface': iface,
                    'type': type
                })


        container = proxmox.nodes(id_node).lxc.get()
        virtual_machine = proxmox.nodes(id_node).qemu.get()

        if container == []:
            container = None
        if virtual_machine == []:
            virtual_machine = None
        

        context = {
            'title': 'Detail Node',
            'active_node': 'active',
            'resource_pool': resource_pool,
            'iso_container': iso_container,
            'iso_virtual_machine' : iso_virtual_machine,
            'network': network,
            'id_node': id_node,
            'container': container,
            'virtual_machine': virtual_machine,
        }
        return render(request, 'node/detail_node.html', context )
    else :
        return('error_connection')
    

# add container 
@login_required(login_url='login')
def addContainer(request, id_node):
    proxmox = get_proxmox()
    if proxmox is not None:
        # id node
        id_node = id_node
        if request.method == "POST":
            ct_id = request.POST.get('ct-id')
            hostname= request.POST.get('hostname')
            resource_pool = request.POST.get('resource-pool')
            password = request.POST.get('password')
            ssh_key = request.POST.get('ssh-key')
            storage_container = request.POST.get('storage-container')
            storage_disk = request.POST.get('storage_disk')
            template = request.POST.get('container_templated')
            disk_size = request.POST.get('disk-size')
            cores = request.POST.get('cores')
            memory = request.POST.get('memory')
            memory_swap = request.POST.get('memory-swap')
            network_interface = request.POST.get('network_interfaces')
            name_network = request.POST.get('name_network')

            # tombol radio static ipv4
            static_ipv4 = request.POST.get('static_ipv4')
            static_ipv6 = request.POST.get('static_ipv6')

            # tombol radio dhcp ipv4
            dhcp_ipv4 = request.POST.get('dhcp_ipv4')
            dhcp_ipv6 = request.POST.get('dhcp_ipv6')

            # data ip address v4
            ip = request.POST.get('ipv4_network')
            gateway = request.POST.get('gateway_network')

            # netmask
            netmask = request.POST.get('netmask')

            #  form required in field
            if not ct_id or not hostname or not password or not template or not network_interface:
                messages.error(request, "Make sure all fields are valid")
                return redirect('detail-node', id_node)
            
            # net0_str = "name=eth0,bridge={network_interface},firewall=1,ip=dhcp"

            # kondisi ketika dhcp ipv4 di centang
            if dhcp_ipv4 == "1":
                net_config = {
                                "name": "eth0",  # Nama antarmuka
                                "bridge": network_interface,  # Nama bridge jika diperlukan
                                "firewall": 1,  # Opsi firewall (1 untuk aktifkan, 0 untuk nonaktifkan)
                                "ip": "dhcp" ,  # Alamat IPv4 (CIDR, dhcp, atau manual)
                                # "gw": gateway,  # Gateway IPv4
                                }
                net0_str = f"name={net_config['name']},bridge={net_config['bridge']},firewall={net_config['firewall']},ip={net_config['ip']}"

                post_data = {
                    "vmid" : ct_id,
                    "ostemplate" : template,
                    "password":password,
                    "cores" : cores,
                    "hostname"  : hostname,
                    "memory" : memory,
                    "swap" : memory_swap,
                    "storage": storage_disk,

                    # interface
                    # "net0": "name=eth0,bridge=vmbr0",  # Use net0 and specify the interface
                    "net0" : net0_str,
                    "pool" : resource_pool,
                    "ssh_public_keys":ssh_key
                }
            # kondisi ketika static ipv4 di centang
            elif static_ipv4 == "1":
                ip_address = ip + '/' + netmask
                net_config = {
                                "name": "eth0",  # Nama antarmuka
                                "bridge": network_interface,  # Nama bridge jika diperlukan
                                "firewall": 1,  # Opsi firewall (1 untuk aktifkan, 0 untuk nonaktifkan)
                                "ip": str(ip_address) ,  # Alamat IPv4 (CIDR, dhcp, atau manual)
                                "gw": str(gateway),  # Gateway IPv4
                                }
                net0_str = f"name={net_config['name']},bridge={net_config['bridge']},firewall={net_config['firewall']},gw={net_config['gw']},ip={net_config['ip']}"

                post_data = {
                    "vmid" : ct_id,
                    "ostemplate" : template,
                    "password":password,
                    "cores" : cores,
                    "hostname"  : hostname,
                    "memory" : memory,
                    "swap" : memory_swap,
                    "storage": storage_disk,

                    # interface
                    # "net0": "name=eth0,bridge=vmbr0",  # Use net0 and specify the interface
                    "net0" : net0_str,
                    "pool" : resource_pool,
                    "ssh_public_keys":ssh_key
                }
            # ketika nilai static dan dhcp ipv4 tidak di centang
            elif static_ipv4 != "1" or dhcp_ipv4 != "1":
                messages.error(request, "Make sure input Interface IPv4")
                return redirect('detail-node', id_node)

            # insert container on proxmox with use api proxoxer
            try:
                proxmox.nodes(id_node).lxc.post(**post_data)
                messages.success(request, "Container added successfully")
                return redirect('detail-node', id_node)
            except Exception as e:
                messages.error(request, f"Error adding container : {str(e)}")
                return redirect('detail-node', id_node)
            
        else:
            # Redirect ke halaman eror jika koneksi gagal
            return redirect('detail-node', id_node)
    else:
        return redirect('error_connection')
    

# add virtual machine 
@login_required(login_url='login')
def addVirtualMachine(request, id_node):
    proxmox = get_proxmox()
    if proxmox is not None:
        # id node
        id_node = id_node
        if request.method == "POST":

            vm_id = request.POST.get('vm-id')
            hostname= request.POST.get('name_vm')
            resource_pool = request.POST.get('resource-pool_vm')
            iso_images = request.POST.get('iso_images')
            ostype = request.POST.get('ostype')

            machine = request.POST.get('machine')
            bios = request.POST.get('bios')
            scsihw = request.POST.get('scsihw')
            # qemuAgent = request.POST.get('qemuAgent')

            storage_virtual_machine = request.POST.get('storage_virtual_machine')
            disk_size_vm = request.POST.get('disk_size_vm')

            sockets = request.POST.get('sockets')
            cores = request.POST.get('cores_vm')

            memory = request.POST.get('memory_vm')

            bridge = request.POST.get('bridge_vm')
            model_network = request.POST.get('model_network')

            # checklist firewall
            if 'firewall_vm' in request.POST:
                    firewall = 1
            else:
                    firewall = 0

            # checklist Qemu Agent
            if 'qemuAgent' in request.POST:
                    qemuAgent = 1
            else:
                    qemuAgent = 0


            # tombol radio static ipv4
            static_ipv4 = request.POST.get('static_ipv4_vm')
            # tombol radio dhcp ipv4
            dhcp_ipv4 = request.POST.get('dhcp_ipv4_vm')

            # data ip address v4
            ipv4 = request.POST.get('ipv4_network_vm')
            netmask = request.POST.get('netmask_vm')
            gateway = request.POST.get('gateway_network_vm')

            #  form required in field
            if not vm_id or not hostname or not iso_images or not bridge:
                messages.error(request, "Make sure all fields are valid")
                return redirect('detail-node', id_node)
            
            
            # kondisi ketika dhcp ipv4 di centang
            if dhcp_ipv4 == "1":

                # net interface objects
                net_config = {
                                "model": model_network,
                                "bridge": bridge,
                                "firewall" : firewall
                            }
                
                net0_str = f"{model_network},bridge={net_config['bridge']},firewall={net_config['firewall']}"
                # ipconfig object
                # ip_address = ipv4 + '/' + netmask
                ip_config = {
                                "ip": "dhcp"  # IP + CIDR
                            }
                
                ip0_str = f"ip={ip_config['ip']}"

                post_data = {
                    "vmid" : vm_id,
                    "name" : hostname,
                    "pool" : resource_pool,
                    "ide2" : iso_images+',media=cdrom',
                    "ostype" : ostype,
                    "machine" : machine,
                    "bios" : bios,
                    "scsihw" : scsihw,
                    "scsi0" : storage_virtual_machine + ':' + disk_size_vm + ',iothread=on',
                    "agent" : qemuAgent,
                    "sockets" : sockets,
                    "cores" : cores,
                    "memory" : memory,
                    "net0" : net0_str,
                    # ipconfig[n]
                    "ipconfig0" : ip0_str
                }
            # kondisi ketika static ipv4 di centang
            elif static_ipv4 == "1":

                # net interface objects
                net_config = {
                                "model": model_network,
                                "bridge": bridge,
                                "firewall" : firewall
                            }
                
                net0_str = f"{model_network},bridge={net_config['bridge']},firewall={net_config['firewall']}"


                # ipconfig object
                ip_address = ipv4 + '/' + netmask
                ip_config = {
                                "ip": ip_address,  # IP + CIDR
                                "gw": gateway  # Gateway IPv4
                            }
                
                ip0_str = f"ip={ip_config['ip']},gw={ip_config['gw']}"

                post_data = {
                    "vmid" : vm_id,
                    "name" : hostname,
                    "pool" : resource_pool,
                    "ide2" : iso_images+',media=cdrom',
                    "ostype" : ostype,
                    "machine" : machine,
                    "bios" : bios,
                    "scsihw" : scsihw,
                    "scsi0" : storage_virtual_machine + ':' + disk_size_vm + ',iothread=on',
                    "agent" : qemuAgent,
                    "sockets" : sockets,
                    "cores" : cores,
                    "memory" : memory,
                    "net0" : net0_str,
                    # ipconfig[n]
                    "ipconfig0" : ip0_str
                }
            # ketika nilai static dan dhcp ipv4 tidak di centang
            elif static_ipv4 != "1" or dhcp_ipv4 != "1":
                messages.error(request, "Make sure input Interface IPv4")
                return redirect('detail-node', id_node)

            # insert virtual machine on proxmox with use api proxoxer
            try:
                proxmox.nodes(id_node).qemu.post(**post_data)
                messages.success(request, "Virtual Machine added successfully")
                return redirect('detail-node', id_node)
            except Exception as e:
                messages.error(request, f"Error adding Virtual Machine : {str(e)}")
                return redirect('detail-node', id_node)
            
        else:
            # Redirect ke halaman eror jika koneksi gagal
            return redirect('detail-node', id_node)
    else:
        return redirect('error_connection')




# start container 
@login_required(login_url='login')
def startContainer(request, id_node, vmid):
    proxmox = get_proxmox()
    time.sleep(1.5)
    if proxmox is not None :
        try:
            proxmox.nodes(id_node).lxc(vmid).status.start.post()
            messages.success(request, "Container started successfully, wait a few moments to start the container")
            return redirect('detail-node', id_node)
        except Exception as e:
            messages.error(request, f"Error starting container : {str(e)}")
            return redirect('detail-node', id_node)
    else :
        return('error_connection')
    
# stop container 
@login_required(login_url='login')
def stopContainer(request, id_node, vmid):
    proxmox = get_proxmox()
    time.sleep(1.5)
    if proxmox is not None :
        try:
            proxmox.nodes(id_node).lxc(vmid).status.stop.post()
            messages.success(request, "Container stopped successfully, wait a few moments to stop the container")
            return redirect('detail-node', id_node)
        except Exception as e:
            messages.error(request, f"Error stoping container : {str(e)}")
            return redirect('detail-node', id_node)
    else :
        return('error_connection')

# reboot container
@login_required(login_url='login')
def rebootContainer(request, id_node, vmid):
    proxmox = get_proxmox()
    time.sleep(1.5)
    if proxmox is not None :
        try:
            proxmox.nodes(id_node).lxc(vmid).status.reboot.post()
            messages.success(request, "Container rebooted successfully, wait a few moments to reboot the container")
            return redirect('detail-node', id_node)
        except Exception as e:
            messages.error(request, f"Error rebooting container : {str(e)}")
            return redirect('detail-node', id_node)
    else :
        return('error_connection')
    
# remove container
@login_required(login_url='login')
def removeContainer(request, id_node, vmid):
    proxmox = get_proxmox()
    time.sleep(1.5)
    if proxmox is not None :
        try:
            proxmox.nodes(id_node).lxc(vmid).delete()
            messages.success(request, "Container removing successfully, wait a few moments to remove the container")
            return redirect('detail-node', id_node)
        except Exception as e:
            messages.error(request, f"Error removing container : {str(e)}")
            return redirect('detail-node', id_node)
    else :
        return('error_connection')
    


# start virtual machine 
@login_required(login_url='login')
def startVirtualMachine(request, id_node, vmid):
    proxmox = get_proxmox()
    time.sleep(1.5)
    if proxmox is not None :
        try:
            proxmox.nodes(id_node).qemu(vmid).status.start.post()
            messages.success(request, "Virtual Machine started successfully, wait a few moments to start the VM")
            return redirect('detail-node', id_node)
        except Exception as e:
            messages.error(request, f"Error starting virtual machine : {str(e)}")
            return redirect('detail-node', id_node)
    else :
        return('error_connection')
    
# stop virtual machine
@login_required(login_url='login')
def stopVirtualMachine(request, id_node, vmid):
    proxmox = get_proxmox()
    time.sleep(1.5)
    if proxmox is not None :
        try:
            proxmox.nodes(id_node).qemu(vmid).status.stop.post()
            messages.success(request, "Virtual Machine stopped successfully, wait a few moments to stop the VM")
            return redirect('detail-node', id_node)
        except Exception as e:
            messages.error(request, f"Error stoping virtual machine : {str(e)}")
            return redirect('detail-node', id_node)
    else :
        return('error_connection')

# reboot virtual machine
@login_required(login_url='login')
def rebootVirtualMachine(request, id_node, vmid):
    proxmox = get_proxmox()
    time.sleep(1.5)
    if proxmox is not None :
        try:
            proxmox.nodes(id_node).qemu(vmid).status.reboot.post()
            messages.success(request, "Virtual Machine rebooted successfully, wait a few moments to reboot the VM")
            return redirect('detail-node', id_node)
        except Exception as e:
            messages.error(request, f"Error rebooting virtual machine : {str(e)}")
            return redirect('detail-node', id_node)
    else :
        return('error_connection')
    

# remove container
@login_required(login_url='login')
def removeVirtualMachine(request, id_node, vmid):
    proxmox = get_proxmox()
    time.sleep(1.5)
    if proxmox is not None :
        try:
            proxmox.nodes(id_node).qemu(vmid).delete()
            messages.success(request, "Virtual Machine removing successfully, wait a few moments to remove the VM")
            return redirect('detail-node', id_node)
        except Exception as e:
            messages.error(request, f"Error removing Virtual Machine : {str(e)}")
            return redirect('detail-node', id_node)
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
        context = {
            'title': 'Profile',
        }
        return render(request, 'settings/profile.html', context )
    else :
        return('error_connection')
    

@login_required(login_url='login')
# halaman profile
def edit_profile(request):
    
    proxmox = get_proxmox()

    if proxmox is not None : 

        # request.user = data sessin ketika sudah login
        user = User.objects.get(id=request.user.id)
        profile = UserProfile.objects.get(user=user)

        if request.method == "POST":
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # update data user
            profile.name = request.POST.get('name')
            user.username = request.POST.get('username')
    
            # jika password tidak diisi
            if not password1 and not password2:
                # maka gunakan password lama
                user.password = user.password
                
                # save
                user.save()
                profile.save()

                messages.success(request, "Your Profile has been updated successfully")
                return redirect('profile')
            else:
                if password1 == password2:
                    # jika password 1 sama dengan password 2
                    # maka ganti password lama dengan password baru
                    # hash password
                    hashed_password = make_password(password1)
                    user.password = hashed_password

                    # save password
                    user.save()

                    messages.success(request, "Your Profile has been updated successfully")
                    return redirect('profile')
                else:
                    messages.error(request, "Password does not match")
                    return redirect('edit-profile')
                    
        context = {
            'title': 'Edit Profile',
            'userData' : user,
            'userProfile': profile
        }
        return render(request, 'settings/edit_profile.html', context )
    else :
        return('error_connection')
    

@login_required(login_url='login')
# update foto profile
def updateImage(request):

    user = User.objects.get(id=request.user.id)

    img = user.profile.avatar
    if request.method == 'POST':

        # hapus  gambar 
        if img and img.storage.exists(img.name):
            img.delete()

        form = UpdateProfileAvatar(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Profile has been updated successfully")
            return redirect('profile')
        else:
            messages.error(request, "Make sure all fields are valid")
            return redirect('edit_profile')



@login_required(login_url='login')
# halaman settings
def settings(request):
    
    proxmox = get_proxmox()

    if proxmox is not None :
        context = {
            'title': 'Settings',
        }
        return render(request, 'settings/setting.html', context )
    else :
        return('error_connection')
    




