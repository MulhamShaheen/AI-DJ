from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', song_list),
    re_path(r'^api/students/(\d+)$', song_detail),
]