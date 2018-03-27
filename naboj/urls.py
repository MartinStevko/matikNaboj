# Debug must be set to false because of 404 and 500 handlers

"""naboj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import handler404, handler500

from obdlznik import views as obdlznik_views
# from trojuholnik import views as trojuholnik_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trojuholnik/', include('trojuholnik.urls')),
    re_path(r'^', include('obdlznik.urls')),
]

handler404 = obdlznik_views.error_404
handler500 = obdlznik_views.error_500

# handler404 = trojuholnik_views.error_404
# handler500 = trojuholnik_views.error_500
