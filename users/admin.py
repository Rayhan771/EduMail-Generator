"""
ব্যবহারকারী অ্যাডমিন কনফিগারেশন - Django Admin প্যানেলে CustomUser দেখানো
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    কাস্টম ইউজার অ্যাডমিন ক্লাস
    Django এর ডিফল্ট UserAdmin কে এক্সটেন্ড করা
    """
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        (_('Account Details'), {
            'fields': ('user_type', 'status', 'profile_picture')
        }),
        (_('Email Verification'), {
            'fields': ('is_email_verified', 'email_verification_token', 'email_verification_token_expires')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'status', 'is_email_verified', 'is_active')
    list_filter = ('user_type', 'status', 'is_email_verified', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at', 'id')
    
    def get_fieldsets(self, request, obj=None):
        """ইউজার আপডেট এর সময় ফিল্ডসেট কাস্টমাইজ করে"""
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
