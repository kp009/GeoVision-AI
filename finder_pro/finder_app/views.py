import os
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from torchvision import transforms
from PIL import Image as PILImage
import math
import torch
import requests
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Image_Loc
from .serializers import Image_LocSerializer, CustomUserSerializer
from .permissions import IsSuperAdmin, IsAdminOrSuperAdmin ,IsUser

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        if user:
            # Generate JWT Token or TokenAuthentication (using simplejwt)
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({
                'access_token': str(access_token),
                'role': user.role  # Assume `role` is a field in the CustomUser model
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# Haversine formula to calculate distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c  # Distance in kilometers
    return distance

def calculate_distance(latitude, longitude):
    # Define a base location (Washington, D.C. in this example)
    base_latitude = 38.8954  # Washington, D.C.
    base_longitude = -77.0369

    # Calculate distance using the Haversine formula
    distance = haversine(base_latitude, base_longitude, latitude, longitude)
    cost = distance * 0.1  # $0.10 per km

    return distance, cost

class ImagePredictor(APIView):
    permission_classes = [IsAuthenticated & (IsAdminOrSuperAdmin | IsUser)]  # Permissions for authenticated users, admins, and superadmins
    
    # File path for model loading
    file_path = (r"C:\Users\suris\location_finder_Pro\location_identifier_model.pth")
    print(file_path)
    # model = torch.load(file_path, map_location=torch.device('cpu'))
    from torchvision import models
    from torchvision.models import MobileNetV2
    import torch

    torch.serialization.add_safe_globals([MobileNetV2])
    # Initialize an empty MobileNetV2 model
    model = models.mobilenet_v2()
    model = torch.load(file_path, weights_only=False)
    # Load the state_dict
    #model.load_state_dict(torch.load(file_path, map_location="cpu"))  

    model.eval()  # Set model to evaluation mode

    # Define label mapping
    label_mapping = {
        "Denmark": 0, "Disney land": 1, "Eiffel-Tower": 2, "Iceland": 3, "Niagara Falls": 4
        # Add other location labels here
    }

    def get_coordinates(self, location_name):
        """Fetch latitude and longitude from OpenStreetMap Nominatim API."""
        try:
            url = f"https://nominatim.openstreetmap.org/search?q={location_name}&format=json"
            headers = {'User-Agent': 'images'}
            response = requests.get(url, headers=headers)
            data = response.json()

            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
            else:
                return None, None
        except Exception as e:
            print(f"Error fetching coordinates: {e}")
            return None, None

    def post(self, request):
        # Ensure proper serializer is used
        serializer = Image_LocSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES['image']

            # Read and preprocess image
            img = PILImage.open(file).convert("RGB")
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
            img = transform(img).unsqueeze(0)  # Add batch dimension

            # Predict location using PyTorch
            with torch.no_grad():
                outputs = self.model(img)
                _, predicted = torch.max(outputs, 1)
                location_index = predicted.item()

            location = list(self.label_mapping.keys())[location_index]

            # Fetch latitude and longitude dynamically
            latitude, longitude = self.get_coordinates(location)

            if latitude is None or longitude is None:
                return Response({"error": "Unable to retrieve coordinates for location."}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate distance and cost
            distance, cost = calculate_distance(latitude, longitude)

            # Save the image and its location data in the database
            image_instance = Image_Loc.objects.create(
                image=file,
                location=location,
                latitude=latitude,
                longitude=longitude,
                distance=distance,
                cost=cost
            )

            # Return the data as a response
            return Response({
                'location': location,
                'latitude': latitude,
                'longitude': longitude,
                'distance': distance,
                'cost': cost
            }, status=status.HTTP_200_OK)

        # If serializer is not valid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageListView(ListAPIView):
    queryset = Image_Loc.objects.all()
    serializer_class = Image_LocSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can view the list

class ImageUpdateView(APIView):
    permission_classes = [IsAuthenticated & (IsAdminOrSuperAdmin)]  # Only admins or superadmins can update

    def put(self, request, pk, *args, **kwargs):
        try:
            image_instance = Image_Loc.objects.get(pk=pk)
        except Image_Loc.DoesNotExist:
            return Response({"error": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = Image_LocSerializer(image_instance, data=request.data, partial=True)  # Partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageDeleteView(APIView):
    permission_classes = [IsAuthenticated & (IsAdminOrSuperAdmin)]  # Only admins or superadmins can delete

    def delete(self, request, pk, *args, **kwargs):
        try:
            image_instance = Image_Loc.objects.get(pk=pk)
        except Image_Loc.DoesNotExist:
            return Response({"error": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

        image_instance.delete()
        return Response({"message": "Image deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

User = get_user_model()

# ---------------- USER MANAGEMENT ---------------- #

class CreateUserView(generics.CreateAPIView):
    """Allows anyone to register."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

class ListUsersView(generics.ListAPIView):
    """Only Admins & SuperAdmins can list users."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminOrSuperAdmin]

class RetrieveUpdateDeleteUserView(generics.RetrieveUpdateDestroyAPIView):
    """Only Super Admins can update/delete users."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsSuperAdmin]

# -------------------------------------------------------- #
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'role': user.role,  # Return the role
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
        })
    


 
