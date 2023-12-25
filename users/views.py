from django.shortcuts import render, redirect
from django.http import HttpResponse

# message flash django
from django.contrib import messages

# django email verify
from django.contrib.auth import login
# from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

# import form apps users
# from users .forms import UserClientForm

# import model apps users
from users .models import Pesanan, HargaPaket

# import model user django
from django.contrib.auth.models import User

# import timezone
from django.utils import timezone

from .tokens import account_activation_token
from django.core.mail import EmailMessage



from django.http import HttpResponseServerError
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


from django.contrib.auth.decorators import user_passes_test


from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

from django.contrib.auth.hashers import make_password  # Import fungsi make_password untuk hash password


# import group 
from django.contrib.auth.models import Group


from django.contrib.auth import logout as auth_logout

# time
import time

from functools import wraps

# Fungsi untuk mengecek apakah pengguna termasuk dalam grup 'user'
def is_user(user):
    return user.groups.filter(name='user').exists() #mengembalikan nilai True jika pengguna termasuk dalam grup 'user'

# Decorator untuk memeriksa akses pengguna ke halaman
def user_access_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Silakan login untuk mengakses halaman ini.")
            return redirect('user_login')
        elif not is_user(request.user):
            messages.error(request, "Akses ditolak. Anda tidak memiliki izin untuk halaman ini.")
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper

# Fungsi untuk melakukan proses login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Lakukan proses otentikasi
        user = authenticate(request, username=username, password=password)
        print(user)
        
        if user is not None:
            if user.groups.filter(name='user').exists():  # Mengecek apakah pengguna termasuk dalam grup 'user'

                # jika user sudah aktif 
                if user.is_active:
                    login(request, user)  # Melakukan login
                    return redirect('dashboard')  # Redirect ke halaman 'about' jika berhasil login dan termasuk dalam grup 'user'
                else:
                    messages.error(request, "Akun anda belum aktif, silahkan cek email anda.")
                    return redirect('user_login')
            else:
                messages.error(request, "Anda tidak memiliki izin untuk login ke sini.")
                return redirect('/')
        else:
            messages.error(request, "Akun belum aktif atau Akun salah.")
            return redirect('user_login')
    
    return render(request, 'login_user.html')  # Menampilkan halaman login jika bukan metode POST

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        name = request.POST.get('name')
        # handphone = request.POST.get('handphone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not email or not name or not password1 or not password2:
            messages.error(request, "Make sure all fields are filled")
            return redirect('sign-up')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('sign-up')
        
        # Check apakah username sudah ada dalam database
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah pernah digunakan. Silakan gunakan username lain.")
            return redirect('sign-up')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email sudah pernah digunakan. Silakan gunakan email lain.")
            return redirect('sign-up')

        try:
            # Buat user Django
            user = User.objects.create_user(username=username, email=email, password=password1, first_name=name, is_active=False, date_joined=timezone.now())
            
            # Mendapatkan atau membuat grup yang diinginkan (misalnya, 'Member')
            group, created = Group.objects.get_or_create(name='user')
            
            # Menambahkan user ke dalam grup yang diinginkan
            group.user_set.add(user)
            
            # Simpan user
            user.save()

            messages.success(request, "Sign up has been successful")
            return redirect('user_login')
            
        except Exception as e:
            messages.error(request, f"Error : {str(e)}")
            return redirect('sign-up')

    return render(request, 'sign-up.html')

def user_logout(request):
    # jika tidak ada session di browser
    if not request.user.is_authenticated:
        # return redirect('error_connection')
        print("tidak ada session di browser")

    # menghapus session di browser
    auth_logout(request)
    time.sleep(1.5)

    messages.success(request, "Anda telah berhasil logout")
    
    return redirect('user_login')

# Gunakan decorator untuk membatasi akses ke view 'about' hanya untuk anggota grup 'user'
# @user_passes_test(is_user)
@user_access_required
def dashboard(request):

    # Mendapatkan data pengguna yang sudah login
    logged_in_user = request.user
    
    # Gunakan informasi pengguna yang didapat, seperti username, email, atau atribut lainnya
    username = logged_in_user.username
    email = logged_in_user.email
    id = logged_in_user.id

    # package price
    package_price = HargaPaket.objects.all()

    # get data pesanan by user id
    pesanan = Pesanan.objects.filter(user_id=id)

    context = {
        'username': username,
        'email': email,
        'id': id,
        'active_dashboard': 'active',
        'package_price': package_price,
        'pesanan' : pesanan,
    }

    # return HttpResponse("About page")
    return render(request, 'pesanan.html', context)

@user_access_required
def user_profile(request, username, id):
    
    # get data user by username and id 
    user = User.objects.get(username=username, id=id)

    context = {
        'user': user,
    }
    return render(request, 'user_profile.html', context)


@user_access_required
def edit_user_profile(request):
    
    # request.user = data sessin ketika sudah login
    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        name = request.POST.get('name')

        user.username = request.POST.get('username')

        # jika password tidak diisi
        if not password1 and not password2:
            # maka gunakan password lama
            user.password = user.password
            user.first_name = name
            
            # save
            user.save()
            messages.success(request, "Profile anda telah berhasil diperbarui")
            return redirect('edit_user_profile')
        else:
            if password1 == password2:
                # jika password 1 sama dengan password 2
                # maka ganti password lama dengan password baru
                # hash password
                hashed_password = make_password(password1)
                user.password = hashed_password
                user.first_name = name
                # save password
                user.save()

                messages.success(request, "Profile anda telah berhasil diperbarui. Silahkan login kembal    i.")
                return redirect('edit_user_profile')
            else:
                messages.error(request, "Password tidak sama")
                return redirect('edit_user_profile')
                
    context = {
        'title': 'Edit Profile',
        'userData' : user,
    }
    return render(request, 'edit_user_profile.html', context )