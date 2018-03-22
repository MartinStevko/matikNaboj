from django.urls import path

from . import views

app_name = 'trojuholnik'

urlpatterns = [
    path('hra', views.druzinka),
    path('body', views.opravovatel),
    path('spravca', views.spravca),
    path('', views.index),
]
