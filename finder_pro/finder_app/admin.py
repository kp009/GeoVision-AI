from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Image_Loc

# Register CustomUser model with custom UserAdmin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

# Register the CustomUser model with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

# Register the Image_Loc model in the admin interface
class Image_LocAdmin(admin.ModelAdmin):
    list_display = ('image', 'location', 'latitude', 'longitude', 'cost', 'distance', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('location', 'description')

# Register the Image_Loc model with the Image_LocAdmin
admin.site.register(Image_Loc, Image_LocAdmin)
