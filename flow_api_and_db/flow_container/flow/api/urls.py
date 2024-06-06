from django.urls import path
from . import views

urlpatterns = [
	path('henriika', views.henriika),
	path('makesoc', views.makesoc),
	path('createuser', views.createuser),
	path('login', views.login),
	path('purgeallusers', views.purgeallusers),
	path('deleteuser', views.deleteuser),
	path('getuser', views.getuser),
	path('avatar', views.avatar),
	path('friend', views.friend),
]
