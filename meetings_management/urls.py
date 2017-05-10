from django.conf.urls import url

from meetings_management.views import (
    EditMeetingRoomView,
    IndexView,
    NewMeetingRoomView,
    NewReservationView,
    EditReservationView,
    LoginView,
    RequestsView,
    signout,
    UsersView,
    RoomsView,
    DeleteReservationView,
    DeleteMeetingRoomView,
    NewRequestView,
    TransferReservationView
)

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', signout, name='logout'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^new_meeting_room/', NewMeetingRoomView.as_view(), name='new-meeting-room'),
    url(r'^edit_meeting_room/(?P<pk>.*)/$', EditMeetingRoomView.as_view(), name='edit-meeting-room'),
    url(r'^delete_meeting_room/(?P<pk>.*)/$', DeleteMeetingRoomView.as_view(), name='delete-meeting-room'),
    url(r'^rooms/', RoomsView.as_view(), name='rooms'),
    url(r'^new_reservation/', NewReservationView.as_view(), name='new-reservation'),
    url(r'^edit_reservation/(?P<pk>.*)/$', EditReservationView.as_view(), name='edit-reservation'),
    url(r'^delete_reservation/(?P<pk>.*)/$', DeleteReservationView.as_view(), name='delete-reservation'),
    url(r'^transfer_reservation/(?P<pk>.*)/$', TransferReservationView.as_view(), name='transfer-reservation'),
    url(r'^requests/', RequestsView.as_view(), name='requests'),
    url(r'^new_request/', NewRequestView.as_view(), name='new-request'),
    url(r'^users/', UsersView.as_view(), name='users')
]
