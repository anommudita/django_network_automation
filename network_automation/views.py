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
        users = proxmox.access.users.get()
        
        context = {
            'title': 'Users',
            'active_user': 'active',
            'users': users,
        }
        return render(request, 'user/user.html', context )
    else:
        # Redirect ke halaman eror jika koneksi gagal
        return redirect('error_connection')

# add user
def  addUser(request):

    # form = UserForm(request.POST, instance = user)
    if request.method == "POST":  
        form = UserForm(request.POST)  
        if form.is_valid():  
            try:  
                

                form.save() 
                # berikan flash message jika berhasi

                messages.success(request, "User added successfully")
                return redirect('user')
            except:  
                # berikan flash message jika gagal
                print(form.errors)
        # form tidak valid atau form tidak isi
        else:
            messages.error(request, "Make sure all fields are valid")
            return redirect('user')
    

# edit user
def editUser(request, id):
    # get data user berdasarkan id
    user = User.objects.get(id=id)  
    return render(request,'user/editUser.html', {'user':user})

def  updateUser(request, id):

    user = User.objects.get(id=id)
    # apakah sesuai dengan method post atau tidak dan data ini dikaitkan dengan data user sebelumnya
    form = UserForm(request.POST, instance = user)
    
    if form.is_valid():
        form.save()
        messages.success(request, "User updated successfully")
        return redirect('user')
    else :
        # berikan flash message jika gagal
        print(form.errors)

    context = {
        'title': 'User',
        'active_user': 'active',
        'form': form

    }
    return render(request, 'user/user.html', context )


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

    permissions = proxmox.access.permissions.get()
    
    context = {
        'title': 'Permissions',
        'active_user': 'active',
        'permissions': permissions,
    }
    return render(request, 'user/permissions.html', context )


#  roles
def  roles(request):

    proxmox = get_proxmox()

    roles = proxmox.access.roles.get()
    
    context = {
        'title': 'Roles',
        'active_user': 'active',
        'roles': roles,
    }
    return render(request, 'user/roles.html', context )

