from django.urls import path
from .views import CameraSetupView, LiveStreamView, DetectedFacesView

urlpatterns = [
    path('', CameraSetupView.as_view(), name='camera_setup'),
    path('live/<int:stream_id>/', LiveStreamView.as_view(), name='live_stream'),
    path('detected/', DetectedFacesView.as_view(), name='detected_faces'),
]