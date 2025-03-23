from rest_framework import serializers
from .models import CustomUser, Image_Loc

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name', 'is_active', 'is_staff']

class Image_LocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image_Loc
        fields = ['id', 'image', 'location', 'latitude', 'longitude', 'cost', 'distance', 'created_at']
