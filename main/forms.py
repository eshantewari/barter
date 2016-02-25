from django.forms import ModelForm
from django import forms

from .models import User, Category, Image, Item, Notification, Address

class UserProfileForm(ModelForm):
    MIN_LENGTH = 8
    first_name = forms.CharField(widget=forms.TextInput(attrs={"onChange":'refresh()'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"onChange":'refresh()'}))
    password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean(self):
        # If the user entered the current password, make sure it's right
        if not self.user.check_password(self.cleaned_data['current_password']):
            raise ValidationError('Your current password is incorrect.')

        # If the user entered the current password, make sure they entered the new passwords as well
        if self.cleaned_data['new_password'] and not (self.cleaned_data['password'] or self.cleaned_data['confirm_password']):
            raise ValidationError('Please enter a new password and a confirmation to update.')

        if self.cleaned_data['new_password'] and self.cleaned_data['confirm_password']:
            password1 = self.cleaned_data.get('new_password')
            password2 = self.cleaned_data.get('confirm_password')
            if password1 != password2:
                raise forms.ValidationError("Your passwords didn't match. Please try again.")

            # At least MIN_LENGTH long
            if len(password1) < self.MIN_LENGTH:
                raise forms.ValidationError("The new password must be at least %d characters long." % self.MIN_LENGTH)

            # At least one letter and one non-letter
            first_isalpha = password1[0].isalpha()
            if all(c.isalpha() == first_isalpha for c in password1):
                raise forms.ValidationError("The new password must contain at least one letter and at least one digit or" \
                                            " punctuation character.")

        return self.cleaned_data

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class CreateUserForm(ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_pic']

    MIN_LENGTH = 8

    def clean(self):

        if self.cleaned_data['new_password'] and not (self.cleaned_data['password'] or self.cleaned_data['confirm_password']):
            raise ValidationError('Please enter a new password and a confirmation.')

        if self.cleaned_data['new_password'] and self.cleaned_data['confirm_password']:
            password1 = self.cleaned_data.get('new_password')
            password2 = self.cleaned_data.get('confirm_password')
            if password1 != password2:
                raise forms.ValidationError("Your passwords didn't match. Please try again.")

            # At least MIN_LENGTH long
            if len(password1) < self.MIN_LENGTH:
                raise forms.ValidationError("The new password must be at least %d characters long." % self.MIN_LENGTH)

            # At least one letter and one non-letter
            first_isalpha = password1[0].isalpha()
            if all(c.isalpha() == first_isalpha for c in password1):
                raise forms.ValidationError("The new password must contain at least one letter and at least one digit or" \
                                            " punctuation character.")


class AddressForm(ModelForm):
    street = forms.CharField(widget=forms.TextInput())
    city = forms.CharField(widget=forms.TextInput())
    zip_code = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = Address
        fields = ['street', 'city', 'zip_code']

    def clean(self):
        return self.cleaned_data

class ItemForm(ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Item
        fields = ['name','description']

    def clean(self):
        return self.cleaned_data

class EditItemForm(ModelForm):
    image2 = forms.ImageField(required=False)
    image3 = forms.ImageField(required=False)

    class Meta:
        model = Item
        fields = ['name','description']

    def clean(self):
        return self.cleaned_data
