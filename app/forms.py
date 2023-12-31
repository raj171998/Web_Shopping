from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from app.models import Customer
from django.contrib.auth import password_validation
class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password  ", widget=forms.PasswordInput(attrs={'class':"form-control"}), required=True)

    password2 = forms.CharField(label="Confirm Password (again) ", widget=forms.PasswordInput(attrs={'class':"form-control"}), required=True)

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels = {'email':"Email"}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}




class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label=_("Password"),widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}), strip=False)

class CustomerProfileForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ['name','locality','city','zipcode','state']

        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
        'locality':forms.TextInput(attrs={'class':'form-control'}),
        'state':forms.Select(attrs={'class':'form-control'}),
        'city':forms.TextInput(attrs={'class':'form-control'}),
        'zipcode':forms.NumberInput(attrs={'class':'form-control'})}

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip = False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))

    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}), help_text=password_validation.password_validators_help_text_html())

    new_password2 = forms.CharField(label=_("Confirm New Password "), strip=False, widget = forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'auto_complete':'reset-password','class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1=forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'auto_complete':'new_password','class':'form-control'}), 
    help_text=password_validation.password_validators_help_text_html())  

    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'auto_complete':'new_password','class':'form-control'}))
