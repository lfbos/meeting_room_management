# coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from meetings_management.models import MeetingRoom, MeetingRoomUser, MeetingRoomReservation


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


class NewRoomForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    location = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))

    capacity = forms.CharField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'min': 1
        }
    ))

    available_from = forms.CharField(widget=forms.DateTimeInput(
        attrs={
            'class': 'form-control'
        }
    ))

    available_until = forms.CharField(widget=forms.DateTimeInput(
        attrs={
            'class': 'form-control'
        }
    ))

    supplies = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'value': 'Proyector,Pizarrón',
            'data-role': 'tagsinput'
        }
    ))


class NewReservationForm(forms.Form):
    meeting_room = forms.ModelChoiceField(
        queryset=MeetingRoom.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    reserved_from = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    reserved_until = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    amount = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'min': 1
            }
        )
    )

    supplies = forms.CharField(
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control'
            }
        )
    )

    confirmed = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput()
    )


class NewRequestForm(forms.Form):
    to_user = forms.ModelChoiceField(
        queryset=MeetingRoomUser.objects.filter(role=0),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    reservation = forms.ModelChoiceField(
        queryset=MeetingRoomReservation.objects.filter(confirmed=False),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    checked = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput()
    )

    reserved_from = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control'}
        )
    )

    reserved_until = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control'}
        )
    )

    amount = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'min': 1
            }
        )
    )

    supplies = forms.CharField(
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control'
            }
        )
    )

    message = forms.CharField(
        max_length=128,
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
        )
    )
