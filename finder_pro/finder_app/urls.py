from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    ImagePredictor,
    ImageListView,
    ImageUpdateView,
    ImageDeleteView,
    CreateUserView,
    ListUsersView,
    RetrieveUpdateDeleteUserView,
    CurrentUserView,
    LoginView,
    )

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    # Image prediction
    path('predict-location/', ImagePredictor.as_view(), name='predict-location'),
    
    # Image location list view
    path('image-locations/', ImageListView.as_view(), name='image-locations-list'),
    
    # Image location update
    path('image-location/<int:pk>/update/', ImageUpdateView.as_view(), name='image-location-update'),
    
    # Image location delete
    path('image-location/<int:pk>/delete/', ImageDeleteView.as_view(), name='image-location-delete'),

     # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   
    #--------
    path('auth/me/', CurrentUserView.as_view(), name='user_info'),  # This endpoint should return user info

    
    # User management
    path('users/', ListUsersView.as_view(), name='users-list'),
    path('user/create/', CreateUserView.as_view(), name='user-create'),
    path('user/<int:pk>/', RetrieveUpdateDeleteUserView.as_view(), name='user-detail-update-delete'),

    
]
