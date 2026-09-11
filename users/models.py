"""
ব্যবহারকারী মডেল - কাস্টম ইউজার মডেল সব ধরনের ব্যবহারকারীর জন্য
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid


class CustomUser(AbstractUser):
    """
    কাস্টম ইউজার মডেল যা AbstractUser থেকে এক্সটেন্ড করা
    সাপোর্ট করে তিন ধরনের ব্যবহারকারী:
    - Super Admin (সিস্টেম অ্যাডমিন)
    - Institution Admin (প্রতিষ্ঠান অ্যাডমিন)
    - Student (শিক্ষার্থী)
    """
    
    USER_TYPE_CHOICES = (
        ('admin', _('Super Admin')),
        ('institution_admin', _('Institution Admin')),
        ('student', _('Student')),
    )
    
    STATUS_CHOICES = (
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('suspended', _('Suspended')),
    )
    
    # ব্যবহারকারী আইডি (UUID)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # ব্যবহারকারীর ধরন
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='student',
        verbose_name=_('User Type')
    )
    
    # ফোন নম্বর
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Phone Number')
    )
    
    # প্রোফাইল ছবি
    profile_picture = models.ImageField(
        upload_to='profile_pics/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name=_('Profile Picture')
    )
    
    # ইমেইল যাচাই করা হয়েছে কি না
    is_email_verified = models.BooleanField(
        default=False,
        verbose_name=_('Email Verified')
    )
    
    # ইমেইল যাচাইকরণ টোকেন
    email_verification_token = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_('Email Verification Token')
    )
    
    # টোকেন মেয়াদোত্তীর্ণ হওয়ার সময়
    email_verification_token_expires = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Token Expiration Time')
    )
    
    # অ্যাকাউন্ট স্ট্যাটাস
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='inactive',
        verbose_name=_('Account Status')
    )
    
    # টাইমস্ট্যাম্প
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )
    
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Deleted At')
    )
    
    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_type']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.user_type})"
    
    def get_full_name(self):
        """সম্পূর্ণ নাম রিটার্ন করে"""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username
    
    def is_admin(self):
        """চেক করে এটা অ্যাডমিন কি না"""
        return self.user_type == 'admin'
    
    def is_institution_admin(self):
        """চেক করে এটা প্রতিষ্ঠান অ্যাডমিন কি না"""
        return self.user_type == 'institution_admin'
    
    def is_student(self):
        """চেক করে এটা শিক্ষার্থী কি না"""
        return self.user_type == 'student'
    
    def is_active_user(self):
        """চেক করে অ্যাকাউন্ট সক্রিয় কি না"""
        return self.status == 'active' and self.is_active
