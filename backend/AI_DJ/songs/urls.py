from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', song_list),
    path('predict/', prompt_prediction),
    re_path(r'^api/songs/(\d+)$', song_detail),
]
