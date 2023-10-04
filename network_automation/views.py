from django.shortcuts import render, redirect

from  network_automation.models import User
from network_automation.forms import UserForm

# time
import time

import json


# message flash django
from django.contrib import messages


# api proxmox
# from proxmoxer import ProxmoxAPI

import paramiko

# Create your views here.


# halaman utama
def home(request):

    context = {
        'title': 'Dashboard',
        'active_home': 'active'
    }
    return render(request, 'base/home.html', context )


#  halaman user
def  user(request):

    host = "192.168.18.125"
    username = "root"
    password = "123123123"
    
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    _stdin, _stdout,_stderr = client.exec_command("pveum user list --output-format json-pretty")

    # print(_stdout.read().decode())
    test_json = _stdout.read().decode()
    client.close()

    test = json.loads(test_json)

    users = User.objects.all()
    
    context = {
        'title': 'User',
        'active_user': 'active',
        'users': users,
        'test' : test
    }
    return render(request, 'base/user.html', context )

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
    return render(request,'base/editUser.html', {'user':user})

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
    return render(request, 'base/user.html', context )


#  delete user
def deleteUser(request, id):
    user = User.objects.get(id=id)
    user.delete()
    time.sleep(1.5)
    return redirect('user')