from django.shortcuts import render, redirect

from  network_automation.models import User
from network_automation.forms import UserForm

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

    users = User.objects.all()
    
    context = {
        'title': 'User',
        'active_user': 'active',
        'users': users
    }
    return render(request, 'base/user.html', context )

# add user
def  addUser(request):

    if request.method == "POST":  
        form = UserForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('user')  
            except:  
                # berikan flash message jika gagal
                pass
    else:  
        form = UserForm()  

    context = {
        'title': 'User',
        'active_user': 'active',
        'form': form

    }
    return render(request, 'base/addUser.html', context )



# edit user
def editUser(request, id):
    # get data user berdasarkan id
    user = User.objects.get(id=id)  
    return render(request,'base/editUser.html', {'user':user})

def  updateUser(request, id):

    user = User.objects.get(id=id)
    # apakah sesuai dengan method post atau tikda 
    form = UserForm(request.POST, instance = user)
    
    if form.is_valid():
        form.save()
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
    return redirect('user')