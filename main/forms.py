from django.forms import ModelForm

from .models import User, Category, Image, Item, SearchField, Notification

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        #Add address

    def clean(self):
        #Check address
        return

class CreateUserForm(ModelForm):
    #Implement Password Checking
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def clean(self):
        #Check address
        return
