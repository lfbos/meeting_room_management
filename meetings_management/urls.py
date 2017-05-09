from django.conf.urls import url

from meetings_management.views import (
    EditMeetingRoomView,
    IndexView,
    NewMeetingRoomView,
    LoginView,
    ReservationsView,
    RequestsView,
    signout,
    UsersView
)

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', signout, name='logout'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^new_meeting_room/', NewMeetingRoomView.as_view(), name='new-meeting-room'),
    url(r'^edit_meeting_room/(?P<pk>.*)/$', EditMeetingRoomView.as_view(), name='edit-meeting-room'),
    url(r'^reservations/', ReservationsView.as_view(), name='reservations'),
    url(r'^requests/', RequestsView.as_view(), name='requests'),
    url(r'^users/', UsersView.as_view(), name='users')
]
