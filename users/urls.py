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
    path('user_profile/<str:username>/<str:id>', views.user_profile, name='user_profile'),

    # route halaman edit profile user
    path('user_profile/settings', views.edit_user_profile, name='edit_user_profile'),
]