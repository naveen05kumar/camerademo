#camera/models.py
from django.db import models
import urllib.parse

class Face(models.Model):
    name = models.CharField(max_length=255, default="Unknown")
    embedding = models.BinaryField()
    image = models.ImageField(upload_to='detected_faces/', default='detected_faces/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.name.startswith("Unknown"):
            max_unknown = Face.objects.filter(name__startswith="Unknown").count()
            self.name = f"Unknown {max_unknown + 1:03d}"
        super().save(*args, **kwargs)

class StaticCamera(models.Model):
    ip_address = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default="Static Camera")

    def rtsp_url(self):
        username = urllib.parse.quote(self.username)
        password = urllib.parse.quote(self.password)
        return f"rtsp://{username}:{password}@{self.ip_address}:1024/Streaming/Channels/101"

class DDNSCamera(models.Model):
    ddns_hostname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default="DDNS Camera")

    def rtsp_url(self):
        username = urllib.parse.quote(self.username)
        password = urllib.parse.quote(self.password)
        return f"rtsp://{username}:{password}@{self.ddns_hostname}:554/Streaming/Channels/101"

class CameraStream(models.Model):
    camera = models.ForeignKey(StaticCamera, null=True, blank=True, on_delete=models.CASCADE)
    ddns_camera = models.ForeignKey(DDNSCamera, null=True, blank=True, on_delete=models.CASCADE)
    stream_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
