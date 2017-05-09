# coding=utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, FormView

from meetings_management.forms import LoginForm, NewRoomForm
from meetings_management.models import (
    MeetingRoom,
    MeetingRoomReservation,
    MeetingRoomUser,
    MeetingRoomRequest
)


class AdminBaseView(LoginRequiredMixin, View):
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
                ),
                'rooms': MeetingRoom.objects.all()
            })
        return super(AdminBaseView, self).get_context_data(**kwargs)

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


class IndexView(AdminBaseView, TemplateView):
    template_name = 'meetings_management/index.html'


class ReservationsView(AdminBaseView, TemplateView):
    template_name = 'meetings_management/reservations.html'
    reservations = None

    def get_context_data(self, **kwargs):
        kwargs = super(ReservationsView, self).get_context_data(**kwargs)
        self.reservations = MeetingRoomReservation.objects.all() \
            if self.request.user.meeting_room_user.role == 1 \
            else self.request.user.meeting_room_user.reservations

        kwargs.update({
            'reservations': self.reservations
        })

        return kwargs


class RequestsView(AdminBaseView, TemplateView):
    template_name = 'meetings_management/requests.html'
    requests = None

    def get_context_data(self, **kwargs):
        kwargs = super(RequestsView, self).get_context_data(**kwargs)
        self.requests = MeetingRoomRequest.objects.all() \
            if self.request.user.meeting_room_user.role == 1 \
            else self.request.user.meeting_room_user.requests

        kwargs.update({
            'requests': self.requests
        })

        return kwargs


class UsersView(AdminBaseView, TemplateView):
    template_name = 'meetings_management/users.html'
    users = None

    def get_context_data(self, **kwargs):
        kwargs = super(UsersView, self).get_context_data(**kwargs)
        if self.request.user.meeting_room_user.role == 1:
            kwargs.update({
                'users': MeetingRoomUser.objects.all()
            })

        return kwargs


class NewMeetingRoomView(AdminBaseView, FormView):
    template_name = 'meetings_management/new_room.html'
    form_class = NewRoomForm
    success_url = '/'

    def form_valid(self, form):
        data = form.cleaned_data
        data['supplies'] = data['supplies'].split(',')

        room = MeetingRoom.objects.create(**data)
        room.refresh_from_db()
        room.save()

        return super(NewMeetingRoomView, self).form_valid(form)


class EditMeetingRoomView(AdminBaseView, FormView):
    template_name = 'meetings_management/edit_room.html'
    form_class = NewRoomForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        kwargs = super(EditMeetingRoomView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        current_room = MeetingRoom.objects.get(pk=pk)
        kwargs.update({
            'current_room': current_room
        })

        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        data['supplies'] = data['supplies'].split(',')

        pk = self.kwargs.get('pk')
        MeetingRoom.objects.filter(pk=pk).update(**data)

        return super(EditMeetingRoomView, self).form_valid(form)


def signout(request):
    logout(request)
    return redirect('app:login')
