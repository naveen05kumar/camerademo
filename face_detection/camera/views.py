#camera/views.py
from django.shortcuts import render, redirect
from django.views import View
from .models import StaticCamera, DDNSCamera, CameraStream, Face
from .serializers import FaceSerializer
from django.http import JsonResponse

class CameraSetupView(View):
    def get(self, request):
        return render(request, 'camera_setup.html')

    def post(self, request):
        camera_type = request.POST.get('camera_type')
        if camera_type == 'static':
            camera = StaticCamera.objects.create(
                ip_address=request.POST.get('ip_address'),
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                name=request.POST.get('name', 'Static Camera')
            )
            rtsp_url = camera.rtsp_url()
        elif camera_type == 'ddns':
            camera = DDNSCamera.objects.create(
                ddns_hostname=request.POST.get('ddns_hostname'),
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                name=request.POST.get('name', 'DDNS Camera')
            )
            rtsp_url = camera.rtsp_url()
        else:
            return JsonResponse({'error': 'Invalid camera type'}, status=400)

        stream = CameraStream.objects.create(
            camera=camera if camera_type == 'static' else None,
            ddns_camera=camera if camera_type == 'ddns' else None,
            stream_url=rtsp_url
        )
        return redirect('live_stream', stream_id=stream.id)

class LiveStreamView(View):
    def get(self, request, stream_id):
        stream = CameraStream.objects.get(id=stream_id)
        return render(request, 'live_stream.html', {'stream_id': stream_id, 'stream_url': stream.stream_url})
class DetectedFacesView(View):
    def get(self, request):
        faces = Face.objects.all().order_by('-created_at')
        stream_id = CameraStream.objects.first().id if CameraStream.objects.exists() else None
        return render(request, 'detected_faces.html', {'faces': faces, 'stream_id': stream_id})

    def post(self, request):
        face_id = request.POST.get('face_id')
        new_name = request.POST.get('new_name')
        face = Face.objects.get(id=face_id)
        face.name = new_name
        face.save()
        return redirect('detected_faces')