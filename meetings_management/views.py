# coding=utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView

from meetings_management.forms import EditRoomForm, LoginForm, NewRoomForm
from meetings_management.models import (
    MeetingRoom,
    MeetingRoomReservation,
    MeetingRoomUser,
    MeetingRoomRequest
)


class AdminBaseView(LoginRequiredMixin, TemplateView):
    login_url = '/app/login/'
    role = None

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated():
            meeting_room_user = MeetingRoomUser.objects.get(user=self.request.user)
            kwargs.update({
                'view_id': self.__class__.__name__.lower(),
                'role': meeting_room_user.role,  # 0 Employee, 1 Admin,
                'username': "{} - {}".format(
                    {
                        0: "Empleado",
                        1: "Administrador"
                    }[meeting_room_user.role],
                    self.request.user.get_full_name() or self.request.user.username
                )
            })
        return super(TemplateView, self).get_context_data(**kwargs)

    class Meta:
        abstract = True


class LoginView(FormView):
    template_name = 'meetings_management/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        if form.has_valid_credentials():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(self.request, user)
                return super(LoginView, self).form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, context={
            'form': form,
            'error': 'Credenciales inválidas, chequee su correo/contraseña'
        })


class IndexView(AdminBaseView):
    template_name = 'meetings_management/index.html'
    rooms = MeetingRoom.objects.all()

    def get_context_data(self, **kwargs):
        kwargs = super(IndexView, self).get_context_data(**kwargs)
        kwargs.update({
            'rooms': self.rooms
        })

        return kwargs


def signout(request):
    logout(request)
    return redirect('app:login')
