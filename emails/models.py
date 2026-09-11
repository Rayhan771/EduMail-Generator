"""
ইমেইল মডেল - ইমেইল অ্যাকাউন্ট এবং জেনারেশন লগ
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from students.models import Student
from institutions.models import Institution
import uuid


class EmailAccount(models.Model):
    """
    ইমেইল অ্যাকাউন্ট মডেল যেখানে জেনারেট করা ইমেইল অ্যাকাউন্ট তথ্য সংরক্ষিত হবে
    """
    
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('active', _('Active')),
        ('suspended', _('Suspended')),
        ('deleted', _('Deleted')),
    )
    
    PROVIDER_CHOICES = (
        ('gmail', _('Gmail')),
        ('outlook', _('Outlook')),
        ('custom', _('Custom Domain')),
    )
    
    # ইমেইল অ্যাকাউন্ট আইডি (UUID)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # শিক্ষার্থীর সাথে সম্পর্ক
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='email_accounts',
        verbose_name=_('Student')
    )
    
    # প্রতিষ্ঠানের সাথে সম্পর্ক
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name='email_accounts',
        verbose_name=_('Institution')
    )
    
    # ইমেইল অ্যাড্রেস
    email_address = models.EmailField(
        unique=True,
        verbose_name=_('Email Address')
    )
    
    # ইমেইল প্রোভাইডার
    provider = models.CharField(
        max_length=20,
        choices=PROVIDER_CHOICES,
        verbose_name=_('Email Provider')
    )
    
    # স্ট্যাটাস
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    
    # পাসওয়ার্ড (এনক্রিপ্টেড)
    password_encrypted = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Encrypted Password')
    )
    
    # রিকভারি ইমেইল
    recovery_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_('Recovery Email')
    )
    
    # ফোন নম্বর (যাচাইকরণের জন্য)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Phone Number')
    )
    
    # প্রোফাইল ছবি URL
    profile_picture_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('Profile Picture URL')
    )
    
    # বায়োগ্রাফি
    biography = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Biography')
    )
    
    # জেনারেশন টাইমস্ট্যাম্প
    generated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Generated At')
    )
    
    # অ্যাক্টিভেশন টাইমস্ট্যাম্প
    activated_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Activated At')
    )
    
    # সাসপেনশন টাইমস্ট্যাম্প
    suspended_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Suspended At')
    )
    
    # ডিলিশন টাইমস্ট্যাম্প
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Deleted At')
    )
    
    # শেষ লগইন
    last_login = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Last Login')
    )
    
    # আপডেট টাইমস্ট্যাম্প
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )
    
    class Meta:
        db_table = 'email_accounts'
        verbose_name = _('Email Account')
        verbose_name_plural = _('Email Accounts')
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['student', 'institution']),
            models.Index(fields=['status']),
            models.Index(fields=['email_address']),
        ]
    
    def __str__(self):
        return f"{self.email_address} ({self.status})"
    
    def is_active(self):
        """চেক করে ইমেইল অ্যাকাউন্ট সক্রিয় কি না"""
        return self.status == 'active'
    
    def is_suspended(self):
        """চেক করে ইমেইল অ্যাকাউন্ট সাসপেন্ড করা হয়েছে কি না"""
        return self.status == 'suspended'
    
    def activate(self):
        """ইমেইল অ্যাকাউন্ট অ্যাক্টিভেট করে"""
        from django.utils import timezone
        self.status = 'active'
        self.activated_at = timezone.now()
        self.save()
    
    def suspend(self):
        """ইমেইল অ্যাকাউন্ট সাসপেন্ড করে"""
        from django.utils import timezone
        self.status = 'suspended'
        self.suspended_at = timezone.now()
        self.save()


class EmailGenerationLog(models.Model):
    """
    ইমেইল জেনারেশন লগ - সব জেনারেশনের ইতিহাস
    """
    
    LOG_TYPE_CHOICES = (
        ('generated', _('Generated')),
        ('activated', _('Activated')),
        ('suspended', _('Suspended')),
        ('deleted', _('Deleted')),
        ('error', _('Error')),
    )
    
    # লগ আইডি (UUID)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # ইমেইল অ্যাকাউন্টের সাথে সম্পর্ক
    email_account = models.ForeignKey(
        EmailAccount,
        on_delete=models.CASCADE,
        related_name='generation_logs',
        verbose_name=_('Email Account')
    )
    
    # লগের ধরন
    log_type = models.CharField(
        max_length=20,
        choices=LOG_TYPE_CHOICES,
        verbose_name=_('Log Type')
    )
    
    # বার্তা/বিবরণ
    message = models.TextField(
        verbose_name=_('Message')
    )
    
    # অতিরিক্ত ডেটা (JSON)
    details = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_('Additional Details')
    )
    
    # টাইমস্ট্যাম্প
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    
    class Meta:
        db_table = 'email_generation_logs'
        verbose_name = _('Email Generation Log')
        verbose_name_plural = _('Email Generation Logs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email_account', 'log_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.email_account.email_address} - {self.log_type}"


class BulkEmailGeneration(models.Model):
    """
    বাল্ক ইমেইল জেনারেশন - একবারে একাধিক ইমেইল জেনারেশন
    """
    
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
    )
    
    # বাল্ক জেনারেশন আইডি (UUID)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # প্রতিষ্ঠানের সাথে সম্পর্ক
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name='bulk_generations',
        verbose_name=_('Institution')
    )
    
    # জেনারেশনের নাম
    name = models.CharField(
        max_length=255,
        verbose_name=_('Generation Name')
    )
    
    # বিবরণ
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Description')
    )
    
    # মোট শিক্ষার্থী সংখ্যা
    total_students = models.IntegerField(
        verbose_name=_('Total Students')
    )
    
    # সফলভাবে জেনারেট করা ইমেইল সংখ্যা
    successful_count = models.IntegerField(
        default=0,
        verbose_name=_('Successful Count')
    )
    
    # ব্যর্থ হওয়া সংখ্যা
    failed_count = models.IntegerField(
        default=0,
        verbose_name=_('Failed Count')
    )
    
    # স্ট্যাটাস
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    
    # টাইমস্ট্যাম্প
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    
    started_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Started At')
    )
    
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Completed At')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )
    
    class Meta:
        db_table = 'bulk_email_generations'
        verbose_name = _('Bulk Email Generation')
        verbose_name_plural = _('Bulk Email Generations')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['institution', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.status})"
    
    def get_progress_percentage(self):
        """জেনারেশনের অগ্রগতি শতাংশ রিটার্ন করে"""
        if self.total_students == 0:
            return 0
        return (self.successful_count / self.total_students) * 100
