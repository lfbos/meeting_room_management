# coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )

    def has_valid_credentials(self):
        try:
            user = get_object_or_404(User, username=self.cleaned_data.get('username'))
            return user.check_password(self.cleaned_data.get('password'))
        except:
            return False


class NewRoomForm(forms.ModelForm):
    pass


class EditRoomForm(forms.ModelForm):
    pass
