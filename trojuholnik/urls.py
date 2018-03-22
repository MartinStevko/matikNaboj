from django.urls import path

from . import views

app_name = 'trojuholnik'

urlpatterns = [
    path('URL_path', views.view_name),
]
