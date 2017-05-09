# coding=utf-8
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

admin.site.site_title = 'Gestión para Salas de Reuniones'
admin.site.site_header = 'Gestión para Salas de Reuniones'
admin.site.index_title = 'Módulos'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app/', include('meetings_management.urls', namespace='app')),
    url(r'^$', RedirectView.as_view(pattern_name='app:index')),
]
