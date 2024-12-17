# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Student,LibraryHistory,FeesHistory

# Customize the admin form for the custom user model
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # List of fields to display in the admin list view
    list_display = ('username', 'email', 'role', 'phone_number', 'address', 'is_staff', 'is_active')
    
    # Fields for search functionality
    search_fields = ('username', 'email', 'role')
    
    # Add additional filters if needed
    list_filter = ('role', 'is_staff', 'is_superuser')
    
    # Fields to show in the detail page (when viewing a user)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields to display when creating/editing a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_superuser')}
        ),
    )
    
    # You can also add inlines for related models if applicable (e.g., profile information)
    # inlines = [YourInlineModelAdmin]

    # Define what fields are required when creating a user
    required_fields = ['email']

# Register the custom user model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(LibraryHistory)
admin.site.register(FeesHistory)
