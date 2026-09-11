"""
শিক্ষার্থী মডেল - শিক্ষার্থীর বিস্তারিত তথ্য সংরক্ষণ
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser
from institutions.models import Institution
import uuid


class Student(models.Model):
    """
    শিক্ষার্থী মডেল যেখানে শিক্ষার্থীর সব তথ্য থাকবে
    প্রতিটি শিক্ষার্থী একটি CustomUser এবং একটি Institution এর সাথে সংযুক্ত
    """
    
    ENROLLMENT_STATUS_CHOICES = (
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('graduated', _('Graduated')),
        ('dropped', _('Dropped')),
    )
    
    GENDER_CHOICES = (
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
    )
    
    # শিক্ষার্থী আইডি (UUID)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # ব্যবহারকারীর সাথে সম্পর্ক
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name=_('User')
    )
    
    # প্রতিষ্ঠানের সাথে সম্পর্ক
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name='students',
        verbose_name=_('Institution')
    )
    
    # শিক্ষার্থী আইডি/রোল নম্বর
    student_id = models.CharField(
        max_length=50,
        verbose_name=_('Student ID/Roll Number')
    )
    
    # প্রোগ্রাম/বিভাগ
    program = models.CharField(
        max_length=255,
        verbose_name=_('Program/Department')
    )
    
    # ব্যাচ/সিমেস্টার
    batch = models.CharField(
        max_length=100,
        verbose_name=_('Batch/Semester')
    )
    
    # জেন্ডার
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        verbose_name=_('Gender')
    )
    
    # জন্ম তারিখ
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Date of Birth')
    )
    
    # যোগাযোগ নম্বর
    contact_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Contact Number')
    )
    
    # জরুরি যোগাযোগ নম্বর
    emergency_contact = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Emergency Contact Number')
    )
    
    # ঠিকানা
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Address')
    )
    
    # এনরোলমেন্ট স্ট্যাটাস
    enrollment_status = models.CharField(
        max_length=20,
        choices=ENROLLMENT_STATUS_CHOICES,
        default='active',
        verbose_name=_('Enrollment Status')
    )
    
    # এনরোলমেন্ট তারিখ
    enrollment_date = models.DateField(
        verbose_name=_('Enrollment Date')
    )
    
    # প্রত্যাশিত স্নাতক তারিখ
    expected_graduation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Expected Graduation Date')
    )
    
    # জিপিএ (সাধারণ জ্ঞান পয়েন্ট গড়)
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_('GPA')
    )
    
    # অতিরিক্ত তথ্য
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Additional Notes')
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
        db_table = 'students'
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        ordering = ['user__first_name', 'user__last_name']
        unique_together = ['institution', 'student_id']
        indexes = [
            models.Index(fields=['institution', 'student_id']),
            models.Index(fields=['enrollment_status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"
    
    def get_full_name(self):
        """সম্পূর্ণ নাম রিটার্ন করে"""
        return self.user.get_full_name()
    
    def get_email(self):
        """শিক্ষার্থীর জেনারেট করা ইমেইল রিটার্ন করে"""
        return self.institution.generate_student_email(
            self.user.first_name,
            self.user.last_name
        )
    
    def is_active(self):
        """চেক করে শিক্ষার্থী সক্রিয় কি না"""
        return self.enrollment_status == 'active'
    
    def is_graduated(self):
        """চেক করে শিক্ষার্থী স্নাতক হয়েছে কি না"""
        return self.enrollment_status == 'graduated'
    
    def get_years_in_program(self):
        """প্রোগ্রামে কতো বছর ছিল তা বের করে"""
        from django.utils import timezone
        today = timezone.now().date()
        days_enrolled = (today - self.enrollment_date).days
        years = days_enrolled / 365.25
        return round(years, 2)
