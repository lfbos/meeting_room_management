# coding=utf-8
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import DeleteView

from meetings_management.exceptions import (
    ReservationCollisionException,
    ReservationReservedCollisionException
)
from meetings_management.forms import (
    LoginForm,
    NewRoomForm,
    NewReservationForm,
    NewRequestForm
)
from meetings_management.models import (
    MeetingRoom,
    MeetingRoomReservation,
    MeetingRoomUser,
    MeetingRoomRequest
)


class AdminBaseView(LoginRequiredMixin, View):
    login_url = '/app/login/'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated():
            meeting_room_user = MeetingRoomUser.objects.get(user=self.request.user)

            user_requests = MeetingRoomRequest.objects.filter(to_user__user=self.request.user)
            user_reservations = MeetingRoomReservation.objects.filter(confirmed=False)

            kwargs.update({
                'view_id': self.__class__.__name__.lower(),
                'role': meeting_room_user.role,  # 0 Employee, 1 Admin,
                'username': "{} - {}".format(
                    {
                        0: "Empleado",
                        1: "Administrador"
                    }[meeting_room_user.role],
                    self.request.user.get_full_name().encode('utf-8') or self.request.user.username
                ),
                'rooms': MeetingRoom.objects.all(),
                'user_requests': user_requests,
                'user_reservations': user_reservations
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


class RoomsView(AdminBaseView, TemplateView):
    template_name = 'meetings_management/rooms.html'


class IndexView(AdminBaseView, TemplateView):
    template_name = 'meetings_management/index.html'

    def get_context_data(self, **kwargs):
        kwargs = super(IndexView, self).get_context_data(**kwargs)
        reservations = MeetingRoomReservation.objects.all()

        kwargs.update({
            'reservations': json.dumps([
                {
                    'pk': str(reservation.pk),
                    'user': reservation.user.user.get_full_name().encode('utf-8') or reservation.user.user.username,
                    'room': {
                        'name': reservation.meeting_room.name,
                        'location': reservation.meeting_room.location,
                    },
                    'reserved_from': reservation.reserved_from.isoformat(),
                    'reserved_until': reservation.reserved_until.isoformat(),
                    'amount': reservation.amount,
                    'supplies': ', '.join(reservation.supplies),
                    'confirmed': reservation.confirmed
                }
                for reservation in reservations.all()
            ])
        })

        return kwargs


class RequestsView(AdminBaseView, TemplateView):
    template_name = 'meetings_management/requests.html'

    def get_context_data(self, **kwargs):
        kwargs = super(RequestsView, self).get_context_data(**kwargs)

        kwargs.update({
            'requests': MeetingRoomRequest.objects.filter(to_user__user=self.request.user),
            'requests_submitted': MeetingRoomRequest.objects.filter(user__user=self.request.user)
        })

        return kwargs


class UsersView(AdminBaseView, TemplateView):
    template_name = 'meetings_management/users.html'

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
    success_url = '/app/rooms/'

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
    success_url = '/app/rooms/'

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


class DeleteMeetingRoomView(DeleteView):
    model = MeetingRoom
    success_url = reverse_lazy('app:rooms')
    template_name = 'meetings_management/room_confirm_delete.html'


class NewReservationView(AdminBaseView, FormView):
    template_name = 'meetings_management/new_reservation.html'
    form_class = NewReservationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        kwargs = super(NewReservationView, self).get_context_data(**kwargs)
        supplies_list = [
            {
                'pk': str(room.pk),
                'list': room.supplies
            }
            for room in MeetingRoom.objects.all()
        ]
        kwargs.update({
            'supplies_list': json.dumps(supplies_list)
        })

        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        data['supplies'] = eval(data['supplies'])
        try:
            data['user'] = self.request.user.meeting_room_user
            MeetingRoomReservation.objects.create(
                **data
            )
        except ReservationCollisionException:
            context = self.get_context_data()
            context.update({
                'error': 'Ya existen reservas confirmadas en el salón: {} que coinciden con esas fechas y horas, '
                         'seleccione otra fecha y hora'.format(
                    form.cleaned_data['meeting_room'].name
                ),
                'form': form
            })
            return render(self.request, self.template_name, context=context)
        except ReservationReservedCollisionException:
            context = self.get_context_data()

            context.update({
                'warning': 'Ya existen reservas en el salón: {}, que coinciden con esas fechas y horas. Si necesita '
                           'usar el salón urgente, contacte con el que reservo para que lo pueda ceder'.format(
                    form.cleaned_data['meeting_room'].name
                ),
                'form': form
            })
            return render(self.request, self.template_name, context=context)
        else:
            return super(NewReservationView, self).form_valid(form)


class EditReservationView(AdminBaseView, FormView):
    template_name = 'meetings_management/edit_reservation.html'
    form_class = NewReservationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        kwargs = super(EditReservationView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')

        supplies_list = [
            {
                'pk': str(room.pk),
                'list': room.supplies
            }
            for room in MeetingRoom.objects.all()
        ]
        kwargs.update({
            'current_reservation': MeetingRoomReservation.objects.get(pk=pk),
            'supplies_list': json.dumps(supplies_list)
        })

        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        data['supplies'] = eval(data['supplies'])

        pk = self.kwargs.get('pk')

        MeetingRoomReservation.objects.filter(pk=pk).update(**data)

        return super(EditReservationView, self).form_valid(form)


class DeleteReservationView(DeleteView):
    model = MeetingRoomReservation
    success_url = reverse_lazy('app:index')
    template_name = 'meetings_management/reservation_confirm_delete.html'


class NewRequestView(AdminBaseView, FormView):
    template_name = 'meetings_management/new_request.html'
    form_class = NewRequestForm
    success_url = '/app/requests/'

    def get_context_data(self, **kwargs):
        kwargs = super(NewRequestView, self).get_context_data(**kwargs)

        supplies_list = [
            {
                'pk': str(room.pk),
                'list': room.supplies
            }
            for room in MeetingRoom.objects.all()
        ]

        reservations = [
            {
                'pk': str(reservation.pk),
                'user': str(reservation.user.pk),
                'name': str(reservation),
                'supplies': reservation.meeting_room.supplies,
                'reserved_from': reservation.reserved_from.isoformat(),
                'reserved_until': reservation.reserved_until.isoformat(),
            }
            for reservation in MeetingRoomReservation.objects.all()
        ]

        kwargs.update({
            'pk': str(MeetingRoomUser.objects.get(user=self.request.user).pk),
            'reservations': json.dumps(reservations),
            'supplies_list': json.dumps(supplies_list)
        })
        return kwargs

    def form_valid(self, form):
        user = MeetingRoomUser.objects.get(user=self.request.user)
        data = form.cleaned_data

        del data['checked']

        data['supplies'] = eval(form.cleaned_data['supplies'])

        try:
            print data
            user.requests.create(**data)
        except Exception as e:
            print e
            context = self.get_context_data()
            context.update({
                'error': 'Ya existe una solicitud para la misma reservación'
            })

            return render(self.request, self.template_name, context=context)
        else:
            return super(NewRequestView, self).form_valid(form)


class TransferReservationView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        request = MeetingRoomRequest.objects.get(pk=pk)

        new_reservation_data = {
            'meeting_room': request.reservation.meeting_room,
            'user': request.user,
            'reserved_from': request.reserved_from,
            'reserved_until': request.reserved_until,
            'amount': request.amount,
            'supplies': request.supplies,
            'confirmed': False
        }

        try:
            # Delete old reservation
            MeetingRoomReservation.objects \
                .filter(pk=request.reservation.pk).delete()

            # Delete request
            MeetingRoomRequest.objects.filter(pk=pk).delete()

            MeetingRoomReservation.objects.create(
                **new_reservation_data
            )
        except Exception as e:
            print e

        return redirect('app:requests')


def signout(request):
    logout(request)
    return redirect('app:login')
