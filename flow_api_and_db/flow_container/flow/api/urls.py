from django.urls import path
from . import views

urlpatterns = [
	path('henriika', views.henriika),
	path('makesoc', views.makesoc),
	path('login', views.login_view),
	path('logout', views.logout_view),
	path('purgeallusers', views.purgeallusers_view),
	path('user', views.user_view),
	path('avatar', views.avatar_view),
	path('friend', views.friend_view),
]
