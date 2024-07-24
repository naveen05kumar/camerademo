#camera/serializers.py
from rest_framework import serializers
from .models import Face
import base64
class FaceSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Face
        fields = ['name', 'image', 'created_at']

    def get_image(self, obj):
        return base64.b64encode(obj.image).decode('utf-8')
