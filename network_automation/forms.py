from django import forms
from network_automation.models import User


# user form
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'password', 'email', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
        }

# # group form
# class GroupForm(forms.ModelForm):
#     class Meta:
#         fields = ['name', 'comment']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'comment': forms.TextInput(attrs={'class': 'form-control'})
#         }