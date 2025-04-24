from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Program, Course, CourseAllocation, Upload

class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed on the admin interface
    list_display = ('username', 'email', 'first_name', 'last_name', 'level', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'level')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Allow editing of password directly in the admin interface (password field is handled by Django)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Custom info'), {'fields': ('level',)}),  # Assuming `level` is a custom field
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'level', 'email'),
        }),
    )
    
    # Define which fields are editable when creating a new user
    def save_model(self, request, obj, form, change):
        if not change:
            # Custom logic when a new user is created
            pass
        super().save_model(request, obj, form, change)

# Register the User model with the custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register the other models
class ProgramAdmin(admin.ModelAdmin):
    pass
class CourseAdmin(admin.ModelAdmin):
    pass
class UploadAdmin(admin.ModelAdmin):
    pass

admin.site.register(Program, ProgramAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseAllocation)
admin.site.register(Upload, UploadAdmin)
