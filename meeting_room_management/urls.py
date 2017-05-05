# coding=utf-8
from django.conf.urls import url
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

admin.site.site_title = 'Gestión para Salas de Reuniones'
admin.site.site_header = 'Gestión para Salas de Reuniones'
admin.site.index_title = 'Módulos'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
