"""
ASGI config for websocket_matches project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

import django
django.setup()

from matchmaking.consumers import MatchConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websocket_matches.settings')

django_asgi_application = get_asgi_application()

websocket_urlpatterns = {
	path('match/connect/<str:game_room>', MatchConsumer.as_asgi()),
}

application = ProtocolTypeRouter({
	'http': django_asgi_application,
	'websocket': URLRouter(websocket_urlpatterns)
})
