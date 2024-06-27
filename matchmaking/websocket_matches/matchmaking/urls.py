from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.urls import include
from . import views
from . import consumers

urlpatterns = [
	path('initiate/', views.initiatematch_view),
]
