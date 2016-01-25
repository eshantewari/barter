from django.forms import ModelForm
from django import forms

from .models import User, Category, Image, Item, Notification, Address

class UserProfileForm(ModelForm):
    #change password
    first_name = forms.CharField(widget=forms.Select(attrs={"onChange":'refresh()'}))
    last_name = forms.CharField(widget=forms.Select(attrs={"onChange":'refresh()'}))
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'Password']

    def clean(self):
        #password validation
        return

class CreateUserForm(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def clean(self):
        #password validation, check username
        return

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'zip_code']

    def clean(self):
        return
