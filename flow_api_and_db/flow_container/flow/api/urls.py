from django.urls import path
from . import views

urlpatterns = [
	path('henriika', views.henriika),
	path('makesoc', views.makesoc),
	path('login', views.login),
	path('purgeallusers', views.purgeallusers),
	path('user', views.user),
	path('avatar', views.avatar),
	path('friend', views.friend),
]
