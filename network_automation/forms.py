from django import forms
from network_automation.models import Server
from django.contrib.auth.models import User
from network_automation.models import UserProfile



# server form
class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ['ip_address', 'username', 'password']
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'comment': forms.TextInput(attrs={'class': 'form-control'})
        # }


class UpdateProfileAvatar(forms.ModelForm):
    avatar = forms.ImageField(help_text="The Avatar field is required.")

    class Meta:
        model = UserProfile
        fields = ('avatar',)

    def __init__(self,*args, **kwargs):
        self.user = kwargs['instance']
        kwargs['instance'] = self.user.profile
        super(UpdateProfileAvatar,self).__init__(*args, **kwargs)


# form update profile (users)
class UpdateProfile(forms.ModelForm):
    username = forms.CharField(max_length=250, help_text="The username field is required")
    password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ['username', 'password']

class UpdateUserProfile(forms.ModelForm):
    name = forms.CharField(max_length=250, help_text="The names field is required")

    class Meta:
        model = UserProfile
        fields = ['name']




# # user form
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['name', 'username', 'password', 'email', 'role']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'password': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.TextInput(attrs={'class': 'form-control'}),
#             'role': forms.TextInput(attrs={'class': 'form-control'}),
#         }

# # # group form
# # class GroupForm(forms.ModelForm):
# #     class Meta:
# #         fields = ['name', 'comment']
# #         widgets = {
# #             'name': forms.TextInput(attrs={'class': 'form-control'}),
# #             'comment': forms.TextInput(attrs={'class': 'form-control'})
# #         }



# add avatar form
# class AddAvatar(forms.ModelForm):
#     # avatar = forms.ImageField(help_text="The Image field is required")
#     # class Meta:
#     #     model = UserProfile
#     #     fields = ['avatar']

#     # clean current password
#     # check apakah password sama dengan password yang lama(database)
#     def clean_current_password(self):
#         current_password = self.cleaned_data['current_password']
#         if not self.instance.check_password(current_password):
#             raise forms.ValidationError("Password is Incorrect.")

# class UpdateProfileMeta(forms.ModelForm):
#     name = forms.CharField(max_length=250, help_text="The name field is required")

#     class Meta:
#         model = UserProfile
#         fields = ['name']