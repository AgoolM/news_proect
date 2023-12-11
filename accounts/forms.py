from typing import Any
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)


# class UserRegistrationForm(forms.Form):
#     password =forms.CharField(label="Parol",
#                             widget=forms.PasswordInput)
#     password_2=forms.CharField(label="Parolni takrorlang",
#                              widget=forms.PasswordInput)

#     class Meta:
#        model=User
#        fields = ['username','first_name',"email"]

#     def clean_password2(self):
#        data = self.cleaned_data
#        if data['password'] != data['password2']:
#           raise forms.ValidationError("Ikkala parolingiz ham bir briga teng bo'lish kerak ")
#        return data['password2']
       
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Parol", widget=forms.PasswordInput)
    password_2 = forms.CharField(label="Parolni takrorlang", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password_2(self):
        data = self.cleaned_data
        if data['password'] != data['password_2']:
            raise forms.ValidationError("Ikkala parolingiz bir-biriga teng bo'lishi kerak")
        return data['password_2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['first_name','last_name','email']




class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth','photo']
