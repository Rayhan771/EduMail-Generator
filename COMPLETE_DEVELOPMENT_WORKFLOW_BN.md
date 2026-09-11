Make these code changes?
COMPLETE_DEVELOPMENT_WORKFLOW_BN.md

md
# 🎓 EduMail Generator - সম্পূর্ণ ডেভেলপমেন্ট ওয়ার্কফ্লো

---

## 📌 **প্রযুক্তি স্ট্যাক চূড়ান্ত নির্ধারণ**

✅ Backend: Python 3.11 + Django 4.2 ✅ Frontend: HTML5 + CSS3 + Bootstrap 5 + JavaScript ✅ Database: PostgreSQL 15 ✅ Email: SendGrid API ✅ Hosting: Heroku / PythonAnywhere (পরে) ✅ Version Control: Git + GitHub

Code

---

# 🔧 **Phase 1: প্রজেক্ট সেটআপ ও কনফিগারেশন**

## **স্টেপ 1.1 - ডেভেলপমেন্ট এনভায়রনমেন্ট সেটআপ**

### প্রয়োজনীয় সফটওয়্যার ইনস্টল করা:
```bash
1. Python 3.11+ ডাউনলোড এবং ইনস্টল
2. PostgreSQL 15 ডাউনলোড এবং ইনস্টল
3. Git ইনস্টল করা
4. Code Editor (VS Code, PyCharm) ইনস্টল
ভার্চুয়াল এনভায়রনমেন্ট তৈরি:
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
প্রয়োজনীয় প্যাকেজ ইনস্টল:
bash
pip install django==4.2
pip install djangorestframework==3.14.0
pip install python-decouple==3.8
pip install psycopg2-binary==2.9.6
pip install sendgrid==6.10.0
pip install pillow==10.0.0
pip install django-cors-headers==4.2.0
pip install requests==2.31.0
স্টেপ 1.2 - Django প্রজেক্ট স্ট্রাকচার তৈরি
প্রজেক্ট এবং অ্যাপ তৈরি:
bash
django-admin startproject config .
python manage.py startapp users
python manage.py startapp institutions
python manage.py startapp students
python manage.py startapp emails
python manage.py startapp core
ফোল্ডার স্ট্রাকচার:
Code
EduMail-Generator/
│
├── config/
│   ├── settings.py          # সব সেটিংস এখানে
│   ├── urls.py              # মেইন URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── users/                   # ব্যবহারকারী ম্যানেজমেন্ট
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── serializers.py
│   └── templates/users/
│
├── institutions/            # প্রতিষ্ঠান ম্যানেজমেন্ট
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/institutions/
│
├── students/                # শিক্ষার্থী ম্যানেজমেন্ট
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/students/
│
├── emails/                  # ইমেইল ম্যানেজমেন্ট
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py          # ইমেইল সেন্ড করার লজিক
│   └── templates/emails/
│
├── core/                    # সাধারণ ফাংশন/utils
│   ├── utils.py
│   ├── decorators.py
│   └── constants.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   └── components/
│
├── .env                     # এনভায়রনমেন্ট ভেরিয়েবল
├── requirements.txt         # প্যাকেজ লিস্ট
├── manage.py
└── db.sqlite3 (পরে PostgreSQL হবে)
স্টেপ 1.3 - ডাটাবেস কনফিগারেশন
PostgreSQL ডাটাবেস তৈরি:
SQL
CREATE DATABASE edumail_generator;
CREATE USER edumail_user WITH PASSWORD 'secure_password_here';
ALTER ROLE edumail_user SET client_encoding TO 'utf8';
ALTER ROLE edumail_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE edumail_user SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE edumail_generator TO edumail_user;
Django settings.py আপডেট:
Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'edumail_generator',
        'USER': 'edumail_user',
        'PASSWORD': 'secure_password_here',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
স্টেপ 1.4 - SendGrid ইমেইল সেটআপ
SendGrid API Key পাওয়া:
Code
1. SendGrid সাইটে যান: https://sendgrid.com
2. ফ্রি অ্যাকাউন্ট তৈরি করুন
3. API Key জেনারেট করুন
4. .env ফাইলে সেভ করুন
.env ফাইল তৈরি:
Code
SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_NAME=edumail_generator
DATABASE_USER=edumail_user
DATABASE_PASSWORD=secure_password_here
DATABASE_HOST=localhost
DATABASE_PORT=5432

SENDGRID_API_KEY=your_sendgrid_api_key_here
SENDGRID_FROM_EMAIL=noreply@edumail-generator.com

EMAIL_BACKEND=sendgrid_backend.SendgridBackend
📊 Phase 2: ডাটাবেস মডেল তৈরি
স্টেপ 2.1 - Users মডেল (ব্যবহারকারী)
Python
# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Super Admin'),
        ('institution_admin', 'Institution Admin'),
        ('student', 'Student'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    email_verification_token_expires = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('inactive', 'Inactive'), ('suspended', 'Suspended')],
        default='inactive'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.user_type})"
স্টেপ 2.2 - Institutions মডেল (প্রতিষ্ঠান)
Python
# institutions/models.py

from django.db import models
from users.models import CustomUser

class Institution(models.Model):
    INSTITUTION_TYPE_CHOICES = (
        ('university', 'University'),
        ('college', 'College'),
    )
    
    name = models.CharField(max_length=255, unique=True)
    institution_type = models.CharField(max_length=20, choices=INSTITUTION_TYPE_CHOICES)
    domain = models.CharField(max_length=100, unique=True)  # e.g., du.edu.bd
    email_format = models.CharField(max_length=255)  # e.g., {first}.{last}@{domain}
    logo = models.ImageField(upload_to='institution_logos/', blank=True, null=True)
    
    # Address Info
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    
    # Contact Info
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    
    # Admin
    admin = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, related_name='institution_admin')
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('active', 'Active'), ('suspended', 'Suspended')],
        default='pending'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'institutions'
        verbose_name_plural = 'Institutions'

    def __str__(self):
        return self.name
স্টেপ 2.3 - Students মডেল (শিক্ষার্থী)
Python
# students/models.py

from django.db import models
from users.models import CustomUser
from institutions.models import Institution

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    DEGREE_CHOICES = (
        ('bachelor', "Bachelor's"),
        ('master', "Master's"),
        ('diploma', 'Diploma'),
    )
    
    SEMESTER_CHOICES = (
        ('spring', 'Spring'),
        ('fall', 'Fall'),
        ('summer', 'Summer'),
    )
    
    # Links
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='students')
    
    # Personal Info
    student_id = models.CharField(max_length=20)  # e.g., 2026001
    registration_no = models.CharField(max_length=50, blank=True, null=True)
    roll_no = models.CharField(max_length=50, blank=True, null=True)
    admission_no = models.CharField(max_length=50, blank=True, null=True)
    
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    
    # Contact Info
    phone = models.CharField(max_length=20)
    alternative_phone = models.CharField(max_length=20, blank=True, null=True)
    personal_email = models.EmailField()
    
    # Address
    country = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    
    # Educational Info
    department = models.CharField(max_length=100)
    program_course = models.CharField(max_length=100)
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    academic_year = models.IntegerField()
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    session = models.CharField(max_length=50)  # e.g., 2026-2027
    
    # Status
    account_status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('inactive', 'Inactive'), ('graduated', 'Graduated')],
        default='inactive'
    )
    
    expected_graduation = models.DateField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'students'
        unique_together = ['institution', 'student_id']
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
স্টেপ 2.4 - EmailAccount মডেল (ইমেইল অ্যাকাউন্ট)
Python
# emails/models.py

from django.db import models
from students.models import Student
from institutions.models import Institution

class EmailAccount(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='email_account')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='email_accounts')
    
    email_address = models.EmailField(unique=True)  # e.g., john.doe@du.edu.bd
    
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('inactive', 'Inactive'), ('suspended', 'Suspended')],
        default='inactive'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'email_accounts'
        verbose_name_plural = 'Email Accounts'

    def __str__(self):
        return self.email_address
স্টেপ 2.5 - EmailInbox মডেল (ইমেইল ইনবক্স)
Python
# emails/models.py (continuation)

class EmailInbox(models.Model):
    email_account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE, related_name='inbox_messages')
    
    from_email = models.EmailField()
    to_email = models.EmailField()
    subject = models.CharField(max_length=255)
    message_body = models.TextField()
    
    is_read = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    
    received_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'email_inbox'
        verbose_name_plural = 'Email Inbox'
        ordering = ['-received_at']

    def __str__(self):
        return f"{self.subject} ({self.from_email})"
🔐 Phase 3: অথেনটিকেশন সিস্টেম
স্টেপ 3.1 - রেজিস্ট্রেশন সিস্টেম
Python
# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.utils import timezone
import uuid
from datetime import timedelta
from .models import CustomUser
from .forms import UserRegistrationForm
from emails.services import send_email

class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # অ্যাকাউন্ট অ্যাক্টিভেশনের জন্য অপেক্ষা
            user.status = 'inactive'
            
            # ইমেইল ভেরিফিকেশন টোকেন তৈরি
            user.email_verification_token = str(uuid.uuid4())
            user.email_verification_token_expires = timezone.now() + timedelta(hours=24)
            user.save()
            
            # ভেরিফিকেশন ইমেইল পাঠান
            send_email(
                recipient=user.email,
                subject="EduMail - ইমেইল ভেরিফিকেশন",
                message=f"আপনার ভেরিফিকেশন কোড: {user.email_verification_token}"
            )
            
            messages.success(request, "রেজিস্ট্রেশন সফল! আপনার ইমেইলে ভেরিফিকেশন কোড পাঠানো হয়েছে।")
            return redirect('verify_email', user_id=user.id)
        
        return render(request, 'users/register.html', {'form': form})
স্টেপ 3.2 - ইমেইল ভেরিফিকেশন
Python
# users/views.py (continuation)

class VerifyEmailView(View):
    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        return render(request, 'users/verify_email.html', {'user': user})
    
    def post(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        verification_code = request.POST.get('verification_code')
        
        if user.email_verification_token == verification_code:
            if timezone.now() < user.email_verification_token_expires:
                user.is_email_verified = True
                user.is_active = True
                user.status = 'active'
                user.email_verification_token = None
                user.email_verification_token_expires = None
                user.save()
                
                messages.success(request, "ইমেইল ভেরিফিকেশন সফল! এখন লগইন করুন।")
                return redirect('login')
            else:
                messages.error(request, "ভেরিফিকেশন কোড মেয়াদ উত্তীর্ণ হয়েছে।")
        else:
            messages.error(request, "ভেরিফিকেশন কোড ভুল।")
        
        return render(request, 'users/verify_email.html', {'user': user})
স্টেপ 3.3 - লগইন সিস্টেম
Python
# users/views.py (continuation)

class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            
            # ব্যবহারকারীর ধরন অনুযায়ী ড্যাশবোর্ডে পাঠান
            if user.user_type == 'admin':
                return redirect('admin_dashboard')
            elif user.user_type == 'institution_admin':
                return redirect('institution_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, "ইমেইল বা পাসওয়ার্ড ভুল।")
        
        return render(request, 'users/login.html')
🤖 Phase 4: অটো ডেটা জেনারেশন (বট)
স্টেপ 4.1 - প্রতিষ্ঠান অটো-জেনারেশন
Python
# core/management/commands/generate_sample_data.py

from django.core.management.base import BaseCommand
from institutions.models import Institution
from users.models import CustomUser
from students.models import Student
from emails.models import EmailAccount
import random

class Command(BaseCommand):
    help = 'অটোমেটিক ডেটা জেনারেট করে'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('ডেটা জেনারেশন শুরু হচ্ছে...'))
        
        # প্রতিষ্ঠান ডেটা
        institutions_data = [
            {
                'name': 'ঢাকা বিশ্ববিদ্যালয়',
                'institution_type': 'university',
                'domain': 'du.edu.bd',
                'email_format': '{first}.{last}@du.edu.bd',
            },
            {
                'name': 'BUET',
                'institution_type': 'university',
                'domain': 'buet.edu.bd',
                'email_format': '{first}.{last}@buet.edu.bd',
            },
            {
                'name': 'NSU',
                'institution_type': 'university',
                'domain': 'nsu.edu.bd',
                'email_format': '{first}.{last}@nsu.edu.bd',
            },
        ]
        
        for inst_data in institutions_data:
            institution, created = Institution.objects.get_or_create(
                name=inst_data['name'],
                defaults={
                    'institution_type': inst_data['institution_type'],
                    'domain': inst_data['domain'],
                    'email_format': inst_data['email_format'],
                    'street_address': '123 Main Street',
                    'city': 'Dhaka',
                    'state_province': 'Dhaka',
                    'postal_code': '1000',
                    'country': 'Bangladesh',
                    'phone': '+880170000000',
                    'email': f'admin@{inst_data["domain"]}',
                    'status': 'active',
                }
            )
            
            if created:
                self.stdout.write(f'✓ তৈরি: {institution.name}')
            else:
                self.stdout.write(f'⊗ ইতিমধ্যে আছে: {institution.name}')
        
        self.stdout.write(self.style.SUCCESS('প্রতিষ্ঠান ডেটা তৈরি সম্পন্ন!'))
স্টেপ 4.2 - শিক্ষার্থী অটো-জেনারেশন
Python
# core/management/commands/generate_sample_data.py (continuation)

import faker

fake = faker.Faker('bn_BD')

def generate_student_data(institution):
    # শিক্ষার্থী ডেটা জেনারেশন
    first_name = fake.first_name()
    last_name = fake.last_name()
    
    # ইমেইল ফরম্যাট অনুযায়ী তৈরি
    email_format = institution.email_format
    email = email_format.format(
        first=first_name.lower(),
        last=last_name.lower(),
        domain=institution.domain
    )
    
    return {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': fake.phone_number(),
        'personal_email': fake.email(),
    }

# ক্রিয়েশনের কোডে যোগ করুন (Command.handle এ)
students_per_institution = 10

for institution in Institution.objects.filter(status='active'):
    for i in range(students_per_institution):
        student_data = generate_student_data(institution)
        
        # ব্যবহারকারী তৈরি
        user = CustomUser.objects.create_user(
            email=student_data['email'],
            password='Student@123',
            first_name=student_data['first_name'],
            last_name=student_data['last_name'],
            user_type='student',
            is_active=True,
            is_email_verified=True,
            status='active',
        )
        
        # শিক্ষার্থী প্রোফাইল তৈরি
        student = Student.objects.create(
            user=user,
            institution=institution,
            student_id=f'{institution.name[:3].upper()}{2026001 + i}',
            first_name=student_data['first_name'],
            last_name=student_data['last_name'],
            phone=student_data['phone'],
            personal_email=student_data['personal_email'],
            country='Bangladesh',
            state_province='Dhaka',
            city='Dhaka',
            postal_code='1000',
            department='Computer Science',
            program_course='BS in CSE',
            degree='bachelor',
            academic_year=2026,
            semester='spring',
            session='2026-2027',
            account_status='active',
        )
        
        # ইমেইল অ্যাকাউন্ট তৈরি
        EmailAccount.objects.create(
            student=student,
            institution=institution,
            email_address=student_data['email'],
            status='active',
        )
        
        self.stdout.write(f'✓ তৈরি: {user.get_full_name()} ({student_data["email"]})')
স্টেপ 4.3 - অটো ডেটা জেনারেশন চালানো
bash
python manage.py generate_sample_data
📧 Phase 5: ইমেইল সার্ভিস ইন্টিগ্রেশন
স্টেপ 5.1 - SendGrid ইমেইল সার্ভিস
Python
# emails/services.py

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
import os
from django.conf import settings

def send_email(recipient, subject, message, html_content=None):
    """
    SendGrid এর মাধ্যমে ইমেইল পাঠান
    
    Args:
        recipient: প্রাপকের ইমেইল
        subject: বিষয়
        message: সাধারণ টেক্সট মেসেজ
        html_content: HTML কন্টেন্ট (অপশনাল)
    """
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        
        from_email = Email(settings.SENDGRID_FROM_EMAIL)
        to_email = To(recipient)
        
        if html_content:
            content = Content("text/html", html_content)
        else:
            content = Content("text/plain", message)
        
        mail = Mail(from_email, to_email, subject, content)
        
        response = sg.send(mail)
        
        print(f"ইমেইল পাঠানো হয়েছে {recipient}কে (Status: {response.status_code})")
        return True
    
    except Exception as e:
        print(f"ইমেইল পাঠাতে ত্রুটি: {str(e)}")
        return False


def send_verification_email(user):
    """ভেরিফিকেশন ইমেইল পাঠান"""
    subject = "EduMail - ইমেইল ভেরিফিকেশন"
    message = f"""
    আপনার ভেরিফিকেশন কোড: {user.email_verification_token}
    
    এটি ২৪ ঘন্টার জন্য বৈধ।
    """
    
    return send_email(user.email, subject, message)


def send_student_credentials_email(student):
    """শিক্ষার্থীকে ইমেইল অ্যাকাউন্ট ক্রেডেনশিয়াল পাঠান"""
    subject = "আপনার প্রাতিষ্ঠানিক ইমেইল অ্যাকাউন্ট প্রস্তুত"
    
    email_account = student.email_account
    
    message = f"""
    প্রিয় {student.first_name},
    
    আপনার প্রাতিষ্ঠানিক ইমেইল অ্যাকাউন্ট তৈরি হয়েছে।
    
    ইমেইল: {email_account.email_address}
    পাসওয়ার্ড: [এটি আপনার অ্যাকাউন্ট পাসওয়ার্ডের সাথে একই]
    
    EduMail Generator
    """
    
    return send_email(student.user.email, subject, message)


def send_institution_approval_email(institution):
    """প্রতিষ্ঠান অনুমোদনের ইমেইল পাঠান"""
    subject = "আপনার প্রতিষ্ঠান অনুমোদিত হয়েছে"
    
    message = f"""
    আপনার প্রতিষ্ঠান {institution.name} অনুমোদিত হয়েছে।
    
    এখন আপনি শিক্ষার্থী ডেটা আপলোড করতে পারবেন।
    """
    
    return send_email(institution.email, subject, message)
🎨 Phase 6: ফ্রন্টএন্ড টেমপ্লেট তৈরি
স্টেপ 6.1 - বেস টেমপ্লেট (Base.html)
HTML
<!-- templates/base.html -->

<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}EduMail Generator{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --success-color: #27ae60;
            --danger-color: #e74c3c;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f7fa;
        }
        
        .navbar {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .navbar-brand {
            font-weight: bold;
            font-size: 1.5rem;
        }
        
        .container-main {
            min-height: calc(100vh - 56px);
            padding: 2rem 0;
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                <i class="bi bi-mortarboard"></i> EduMail Generator
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="/dashboard/">
                                <i class="bi bi-speedometer2"></i> ড্যাশবোর্ড
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/profile/">
                                <i class="bi bi-person-circle"></i> প্রোফাইল
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/logout/">
                                <i class="bi bi-box-arrow-right"></i> লগআউট
                            </a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="/login/">লগইন</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/register/">রেজিস্টার</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>
    
    <!-- Messages -->
    <div class="container-fluid mt-3">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}
    </div>
    
    <!-- Main Content -->
    <main class="container-main">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-4 mt-5">
        <p>&copy; 2024 EduMail Generator. সকল অধিকার সংরক্ষিত।</p>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
স্টেপ 6.2 - লগইন পেজ
HTML
<!-- templates/users/login.html -->

{% extends 'base.html' %}

{% block title %}লগইন - EduMail Generator{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center mt-5">
        <div class="col-md-5">
            <div class="card shadow-lg">
                <div class="card-body p-5">
                    <h2 class="card-title text-center mb-4">
                        <i class="bi bi-box-arrow-in-right"></i> লগইন করুন
                    </h2>
                    
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label for="email" class="form-label">ইমেইল</label>
                            <input type="email" class="form-control" id="email" name="email" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="password" class="form-label">পাসওয়ার্ড</label>
                            <input type="password" class="form-control" id="password" name="password" required>
                        </div>
                        
                        <button type="submit" class="btn btn-primary w-100">লগইন</button>
                    </form>
                    
                    <hr>
                    
                    <p class="text-center">
                        এখনও অ্যাকাউন্ট নেই? 
                        <a href="/register/">রেজিস্টার করুন</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
স্টেপ 6.3 - শিক্ষার্থী ড্যাশবোর্ড
HTML
<!-- templates/students/dashboard.html -->

{% extends 'base.html' %}

{% block title %}শিক্ষার্থী ড্যাশবোর্ড{% endblock %}

{% block content %}
<div class="container">
    <h1 class="mb-4">
        <i class="bi bi-person"></i> স্বাগতম, {{ user.get_full_name }}
    </h1>
    
    <div class="row">
        <!-- অ্যাকাউন্ট তথ্য -->
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <i class="bi bi-info-circle"></i> অ্যাকাউন্ট তথ্য
                </div>
                <div class="card-body">
                    <p><strong>নাম:</strong> {{ student.first_name }} {{ student.last_name }}</p>
                    <p><strong>স্টুডেন্ট আইডি:</strong> {{ student.student_id }}</p>
                    <p><strong>প্রতিষ্ঠান:</strong> {{ student.institution.name }}</p>
                    <p><strong>বিভাগ:</strong> {{ student.department }}</p>
                    <p><strong>অ্যাকাউন্ট স্ট্যাটাস:</strong> 
                        {% if student.account_status == 'active' %}
                            <span class="badge bg-success">সক্রিয়</span>
                        {% else %}
                            <span class="badge bg-danger">নিষ্ক্রিয়</span>
                        {% endif %}
                    </p>
                </div>
            </div>
        </div>
        
        <!-- ইমেইল অ্যাকাউন্ট -->
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-success text-white">
                    <i class="bi bi-envelope"></i> ইমেইল অ্যাকাউন্ট
                </div>
                <div class="card-body">
                    <p><strong>ইমেইল:</strong> {{ email_account.email_address }}</p>
                    <p><strong>স্ট্যাটাস:</strong>
                        {% if email_account.status == 'active' %}
                            <span class="badge bg-success">সক্রিয়</span>
                        {% else %}
                            <span class="badge bg-danger">নিষ্ক্রিয়</span>
                        {% endif %}
                    </p>
                    <p><strong>তৈরি:</strong> {{ email_account.created_at|date:"d/m/Y" }}</p>
                    <a href="{% url 'email_inbox' %}" class="btn btn-sm btn-primary">
                        <i class="bi bi-inbox"></i> ইনবক্স দেখুন
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    <!-- ইনবক্স প্রিভিউ -->
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header bg-info text-white">
                    <i class="bi bi-inbox"></i> সম্প্রতি মেইলস
                </div>
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead class="table-light">
                            <tr>
                                <th>থেকে</th>
                                <th>বিষয়</th>
                                <th>তারিখ</th>
                                <th>অ্যাকশন</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for message in recent_messages %}
                                <tr>
                                    <td>{{ message.from_email }}</td>
                                    <td>{{ message.subject }}</td>
                                    <td>{{ message.received_at|date:"d/m/Y H:i" }}</td>
                                    <td>
                                        <a href="{% url 'email_detail' message.id %}" class="btn btn-sm btn-outline-primary">
                                            <i class="bi bi-eye"></i>
                                        </a>
                                    </td>
                                </tr>
                            {% empty %}
                                <tr>
                                    <td colspan="4" class="text-center text-muted">কোন মেইল নেই</td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
🔗 Phase 7: URL রুটিং
স্টেপ 7.1 - মেইন URL (config/urls.py)
Python
# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('users/', include('users.urls')),
    path('institutions/', include('institutions.urls')),
    path('students/', include('students.urls')),
    path('emails/', include('emails.urls')),
]
স্টেপ 7.2 - ব্যবহারকারী URL (users/urls.py)
Python
# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify-email/<int:user_id>/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
🗄️ Phase 8: ডাটাবেস মাইগ্রেশন
bash
# মাইগ্রেশন ফাইল তৈরি করুন
python manage.py makemigrations

# মাইগ্রেশন প্রয়োগ করুন
python manage.py migrate

# সুপার অ্যাডমিন তৈরি করুন
python manage.py createsuperuser

# অটো ডেটা জেনারেট করুন
python manage.py generate_sample_data

# সার্ভার চালু করুন
python manage.py runserver
✅ সম্পূর্ণ কাজের চেকলিস্ট
Backend সম্পন্ন:
 Django প্রজেক্ট সেটআপ
 PostgreSQL ডাটাবেস সংযোগ
 ডাটা মডেল তৈরি
 ব্যবহারকারী অথেনটিকেশন
 ইমেইল ভেরিফিকেশন
 SendGrid ইন্টিগ্রেশন
 অটো ডেটা জেনারেশন
 API এন্ডপয়েন্ট
Frontend সম্পন্ন:
 HTML টেমপ্লেট
 CSS স্টাইলিং (Bootstrap)
 রেজিস্ট্রেশন পেজ
 লগইন পেজ
 ড্যাশবোর্ড পেজ
 ইনবক্স পেজ
ফিচার সম্পন্ন:
 প্রতিষ্ঠান ম্যানেজমেন্ট
 শিক্ষার্থী ম্যানেজমেন্ট
 ইমেইল অ্যাকাউন্ট জেনারেশন
 ইমেইল ইনবক্স সিস্টেম
 অ্যাডমিন ড্যাশবোর্ড
ডিপ্লয়মেন্ট প্রস্তুত:
 পারফরম্যান্স অপটিমাইজেশন
 সিকিউরিটি অডিট
 ইউনিট টেস্টিং
 Heroku/AWS ডিপ্লয়মেন্ট
🎯 এখন আপনার সম্মতি দিন:
আপনি কি এই সম্পূর্ণ ওয়ার্কফ্লো অনুযায়ী কাজ শুরু করতে প্রস্তুত?

"হ্যাঁ" বলুন, আমরা শুরু করব! ✅🚀

Code
