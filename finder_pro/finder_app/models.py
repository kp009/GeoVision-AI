from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser"""
    
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('role', 'user')  # Ensure role is set for regular users
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, username, email, password=None, **extra_fields):
        """Create and return an admin user."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'admin')  # Set role explicitly
        return self.create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create a superuser with all permissions."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superadmin')  # Explicitly set role

        if extra_fields.get('is_staff') is not True or extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_staff=True and is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')

    objects = CustomUserManager()  # Attach the custom manager

    def is_admin(self):
        return self.role in ['admin', 'superadmin']

    def is_superadmin(self):
        return self.role == 'superadmin'
    
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    def __str__(self):
        return self.username


class Image_Loc(models.Model):
    image = models.ImageField(upload_to='uploads/')
    location = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Cost associated with the image
    distance = models.FloatField(null=True, blank=True)  # Distance in miles/km
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the image was uploaded

    def __str__(self):
        return f"{self.image.name} - {self.location if self.location else 'Unknown Location'}"
