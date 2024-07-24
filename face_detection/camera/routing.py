from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/camera/(?P<stream_id>[^/]+)/$', consumers.CameraConsumer.as_asgi()),
]