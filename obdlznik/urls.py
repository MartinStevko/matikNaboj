from django.urls import path, re_path

from . import views

app_name = 'trojuholnik'

urlpatterns = [
    path('obdlznik/login/', views.log_in),
    path('obdlznik/logout/', views.logout_page),
    path('obdlznik/logout/request/user/', views.log_out),
    path('obdlznik/hra/', views.druzinka),
    path('obdlznik/ulohy/', views.opravovatel),
    path('obdlznik/spravca/', views.spravca),
    path('obdlznik/', views.index),
    re_path(r'^', views.error_404),
]
