from django.urls import path, re_path

from . import views

app_name = 'trojuholnik'

urlpatterns = [
    path('hra', views.druzinka),
    path('body', views.opravovatel),
    path('spravca', views.spravca),
    re_path(r'^', views.error_404)
]
