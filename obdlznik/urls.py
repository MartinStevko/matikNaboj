from django.urls import path, re_path

from . import views

app_name = 'trojuholnik'

urlpatterns = [
    path('obdlznik/hra', views.druzinka),
    path('obdlznik/ulohy', views.opravovatel),
    path('obdlznik/spravca', views.spravca),
    re_path(r'^', views.error_404)
]
