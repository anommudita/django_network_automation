from django.urls import path
from users import views

urlpatterns = [
    # route login user
    path('', views.user_login, name='user_login'),

    # route login required
    path('account/login', views.user_login, name='login_required'),

    # route logout user
    path('logout', views.user_logout, name='user_logout'),

    # route register user
    path('sign-up', views.register, name='sign-up'),

    # route halaman dasboard
    path('dashboard', views.dashboard, name='dashboard'),

    # route halaman profile user
    path('user_profile/<str:username>/<str:id>/', views.user_profile, name='user_profile'),

    # route halaman edit profile user
    path('user_profile/settings', views.edit_user_profile, name='edit_user_profile'),

    # route untuk membuat pesanan sesuai paket
    path('pesanan_user/<str:cpu>/<str:ram>/<str:storage>/<str:id_paket>', views.pesanan_sesuai_paket, name='pesanan_user'),

    # route untuk membuat pesanan sesuai paket
    path('pesanan_custom', views.pesananCustom, name='pesanan_custom'),

    path('data_api_user', views.data_api_user, name='data_api_user'),

    # route halaman delete order by user
    path('delete-order-by-user/<str:id_order>', views.deleteOrderbyUser, name='delete-order-by-user'),
]