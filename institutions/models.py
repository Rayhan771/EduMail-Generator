"""
প্রতিষ্ঠান মডেল - বিশ্ববিদ্যালয় এবং কলেজের তথ্য সংরক্ষণ
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser
import uuid


class Institution(models.Model):
    """
    প্রতিষ্ঠান মডেল যেখানে বিশ্ববিদ্যালয় এবং কলেজের সব তথ্য থাকবে
    প্রতিটি প্রতিষ্ঠানের নিজস্ব ইমেইল ডোমেইন এবং ফরম্যাট থাকবে
    """
    
    INSTITUTION_TYPE_CHOICES = (
        ('university', _('University')),
        ('college', _('College')),
    )
    
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('active', _('Active')),
        ('suspended', _('Suspended')),
    )
    
    # প্রতিষ্ঠান আইডি (UUID)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # প্রতিষ্ঠানের নাম
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('Institution Name')
    )
    
    # প্রতিষ্ঠানের ধরন
    institution_type = models.CharField(
        max_length=20,
        choices=INSTITUTION_TYPE_CHOICES,
        verbose_name=_('Institution Type')
    )
    
    # ইমেইল ডোমেইন (যেমন: du.edu.bd)
    domain = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Email Domain')
    )
    
    # ইমেইল ফরম্যাট (যেমন: {first}.{last}@{domain})
    email_format = models.CharField(
        max_length=255,
        verbose_name=_('Email Format'),
        help_text=_('Use {first}, {last}, {domain} as placeholders')
    )
    
    # লোগো
    logo = models.ImageField(
        upload_to='institution_logos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name=_('Institution Logo')
    )
    
    # ঠিকানা তথ্য
    street_address = models.CharField(
        max_length=255,
        verbose_name=_('Street Address')
    )
    
    city = models.CharField(
        max_length=100,
        verbose_name=_('City')
    )
    
    state_province = models.CharField(
        max_length=100,
        verbose_name=_('State/Province')
    )
    
    postal_code = models.CharField(
        max_length=20,
        verbose_name=_('Postal Code')
    )
    
    country = models.CharField(
        max_length=100,
        verbose_name=_('Country')
    )
    
    # যোগাযোগ তথ্য
    phone = models.CharField(
        max_length=20,
        verbose_name=_('Phone Number')
    )
    
    email = models.EmailField(
        verbose_name=_('Email Address')
    )
    
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('Website')
    )
    
    # অ্যাডমিন ব্যবহারকারী
    admin = models.OneToOneField(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='managed_institution',
        verbose_name=_('Institution Admin')
    )
    
    # প্রতিষ্ঠানের স্ট্যাটাস
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    
    # বর্ণনা
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Description')
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
        db_table = 'institutions'
        verbose_name = _('Institution')
        verbose_name_plural = _('Institutions')
        ordering = ['name']
        indexes = [
            models.Index(fields=['domain']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.institution_type})"
    
    def get_email_format_display(self):
        """ইমেইল ফরম্যাট প্রদর্শন করে"""
        return self.email_format.replace('{domain}', self.domain)
    
    def generate_student_email(self, first_name, last_name):
        """
        শিক্ষার্থীর ইমেইল অ্যাড্রেস জেনারেট করে
        
        Args:
            first_name: প্রথম নাম
            last_name: শেষ নাম
            
        Returns:
            জেনারেট করা ইমেইল অ্যাড্রেস
        """
        email = self.email_format.format(
            first=first_name.lower(),
            last=last_name.lower(),
            domain=self.domain
        )
        return email
    
    def get_total_students(self):
        """মোট শিক্ষার্থী সংখ্যা রিটার্ন করে"""
        return self.students.count()
    
    def get_active_students(self):
        """সক্রিয় শিক্ষার্থী সংখ্যা রিটার্ন করে"""
        return self.students.filter(account_status='active').count()
    
    def get_active_email_accounts(self):
        """সক্রিয় ইমেইল অ্যাকাউন্ট সংখ্যা রিটার্ন করে"""
        return self.email_accounts.filter(status='active').count()
