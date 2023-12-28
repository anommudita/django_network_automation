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

# from django.contrib.auth import authenticate, login as auth_login_user
from django.shortcuts import redirect, render
from django.contrib import messages

from django.contrib.auth.hashers import make_password  # Import fungsi make_password untuk hash password


# import group 
from django.contrib.auth.models import Group


from django.contrib.auth import logout as auth_logout

# time
import time

from functools import wraps

import random

# django pdf
from django_xhtml2pdf.utils import pdf_decorator

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io

import datetime

# Fungsi untuk mengecek apakah pengguna termasuk dalam grup 'user'
def is_user(user):
    return user.groups.filter(name='user').exists() #mengembalikan nilai True jika pengguna termasuk dalam grup 'user'

# get response json
from django.http import JsonResponse


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
        # print(user)
        
        if user is not None:
            if user.groups.filter(name='user').exists():  # Mengecek apakah pengguna termasuk dalam grup 'user'
                # jika user sudah aktif 
                if user.is_active:
                    login(request, user)  # Melakukan login
                    # auth_login_user(request, user)
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
            messages.error(request, "Pastikan semua kolom terisi")
            return redirect('sign-up')

        if password1 != password2:
            messages.error(request, "Kata sandi tidak sama")
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

@user_access_required
def data_api_user(request):
    action = request.GET.get('action')
    try:
        match action:
            case 'view_data_pesanan':
                id = request.GET.get('id')
                
                # get data pesanan by id
                pesanan = Pesanan.objects.get(id=id)
                order = {
                    'id': pesanan.id,
                    'user_id': pesanan.user_id,
                    'harga_paket_id': pesanan.harga_paket_id,
                    'core': pesanan.core,
                    'ram': pesanan.ram,
                    'storage': pesanan.storage,
                    'username': pesanan.username,
                    'password': pesanan.password,
                    'os': pesanan.os,
                    'perbulan': pesanan.perbulan,
                    'jenis': pesanan.jenis,
                }
                response = {
                    'status': 'success',
                    'message': 'Data successfully retrieved',
                    'data': order
                }
                return JsonResponse(response)       
    except Exception as e:
            return HttpResponse(f"Error : {str(e)}", status=500)
    



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
    package_price = HargaPaket.objects.all()[:3]

    # get data pesanan by user id
    pesanan = Pesanan.objects.filter(user_id=id)


    users = User.objects.exclude(is_superuser=True)

    context = {
        'username': username,
        'email': email,
        'id': id,
        'active_dashboard': 'active',
        'package_price': package_price,
        'pesanan' : pesanan,
        'users': users,
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


@user_access_required
def pesanan_sesuai_paket(request, cpu, ram, storage, id_paket):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        penyewaan = request.POST.get('penyewaan')
        os = request.POST.get('paket_os')

        if not username or not password or not penyewaan :
            messages.error(request, "Pastikan semua kolom terisi")
            return redirect('dashboard')
        
        try:

            current_user = request.user

            current_paket = HargaPaket.objects.get(id=id_paket)

            # membuat order
            order = Pesanan.objects.create(
                user=current_user, harga_paket=current_paket, core=cpu, ram=ram, storage=storage, username=username, password=password, os=os, perbulan=penyewaan, jenis="container")
            
            # Simpan  orderan
            order.save()

            messages.success(request, "Pesanan anda telah berhasil dibuat, tunggu admin untuk mengaktifkan pesanan anda:)")
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f"Error : {str(e)}")
            return redirect('dashboard')


@user_access_required
def deleteOrderbyUser(request, id_order):
    try:
        # delete data user to database
        order = Pesanan.objects.get(id=id_order)
        order.delete()
        time.sleep(1.5)
        messages.success(request, "Order telah berhasil dihapus")
        return redirect('dashboard')
    except Exception as e:
        messages.error(request, f"Error deleted order : {str(e)}")
        return redirect('dashboard')
    


def gb_to_mb(gb):
    mb = gb * 1024  # 1 GB = 1024 MB
    return mb


@user_access_required
def pesananCustom(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        penyewaan = request.POST.get('penyewaan')
        cpu = request.POST.get('cpu')
        storage = request.POST.get('storage')
        ram = request.POST.get('ram')
        os = request.POST.get('os')

        memory = gb_to_mb(int(ram))

        if not username or not password or not penyewaan or not cpu or not storage or not ram or not os:
            messages.error(request, "Pastikan semua kolom terisi")
            return redirect('dashboard')
        
        try:

            current_user = request.user

            last_paket = HargaPaket.objects.latest('id')

            # membuat order
            order = Pesanan.objects.create(
                user=current_user, harga_paket=last_paket, core=cpu, ram=memory, storage=storage, username=username, password=password, os=os, perbulan=penyewaan, jenis="container")
            
            # Simpan  orderan
            order.save()

            messages.success(request, "Pesanan anda telah berhasil dibuat, tunggu admin untuk mengaktifkan pesanan anda:)")
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f"Error : {str(e)}")
            return redirect('dashboard')
        
def updatePesanan(request, id_order):
    if request.method == "POST":
        username = request.POST.get('edit_username')
        password = request.POST.get('edit_password')
        penyewaan = request.POST.get('edit_penyewaan')
        cpu = request.POST.get('edit_cpu')
        storage = request.POST.get('edit_storage')
        ram = request.POST.get('edit_ram')
        os = request.POST.get('edit_os')


        memory = gb_to_mb(int(ram))

        if not username or not password :
            messages.error(request, "Make sure all fields are valid")
            return redirect('dashboard')
        try:
            current_user = request.user

            order = Pesanan.objects.get(id=id_order)
            order.core = cpu
            order.ram = ram
            order.storage = storage
            order.username = username
            order.password = password
            order.os = os
            order.perbulan = penyewaan
            order.jenis = "container"
            order.user = current_user
            # Simpan  orderan
            order.save()

            messages.success(request, "Pesanan anda telah berhasil diedit, tunggu admin untuk mengaktifkan pesanan anda:)")
            return redirect('dashboard')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('dashboard')      
        


@pdf_decorator(pdfname='invoice.pdf')
def printInvoiceUser(request, id_invoice):

    order = Pesanan.objects.get(id=id_invoice)

    harga_paket = float(order.harga_paket.harga.replace('.', '').replace(',', '.'))  # Ubah string menjadi float
    total = harga_paket * int(order.perbulan)
    total_str = '{:,.0f}'.format(total).replace(',', '.')  # Ubah nilai menjadi string dengan format yang diinginkan

    # Generate angka acak antara 100000 dan 999999
    progress_kode_random = random.randint(100000, 999999)

    # Membuat kode invoice dengan menggabungkan string dan angka acak
    kode_invoice = f"CEG-{progress_kode_random}"

    # Menggabungkan ke dalam format yang diinginkan
    tanggal_baru = order.date_created.strftime("%d/%m/%Y")

    todayThis = datetime.date.today()
    today = todayThis.strftime("%d/%m/%Y")

    if order.status == "0":
        status = "Belum di proses"
    else :
        status = "Sudah di proses"


    context = {
        'order' : order,
        'total' : total_str,
        'today' : today,
        'date_created' : tanggal_baru,
        'kode_invoice' : kode_invoice,
        'status' : status,
    }
    return render(request, 'invoice/invoice.html', context)
