from django import forms
from users.models import UserClient
from django.contrib.auth.models import User


# update profile client
# class UpdateProfileAvatar(forms.ModelForm):
#     avatar = forms.ImageField(help_text="The Avatar field is required.")

#     class Meta:
#         model = UserProfile
#         fields = ('avatar',)

#     def __init__(self,*args, **kwargs):
#         self.user = kwargs['instance']
#         kwargs['instance'] = self.user.profile
#         super(UpdateProfileAvatar,self).__init__(*args, **kwargs)


# form update profile (users)
class UserClientForm(forms.ModelForm):
    username = forms.CharField(max_length=250, help_text="The username field is required")
    password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ['username', 'password']


# update user sclient
class UpdateUserClient(forms.ModelForm):
    name = forms.CharField(max_length=250, help_text="The names field is required")
    no_hp = forms.CharField(max_length=250, help_text="The number handphone field is required")
    class Meta:
        model = UserClient
        fields = ['name']



