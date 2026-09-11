"""
EduMail Generator - মেইন URL কনফিগারেশন
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # অ্যাডমিন প্যানেল
    path('admin/', admin.site.urls),
    
    # হোমপেজ
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # ব্যবহারকারী সম্পর্কিত URL
    path('users/', include('users.urls')),
    
    # প্রতিষ্ঠান সম্পর্কিত URL
    path('institutions/', include('institutions.urls')),
    
    # শিক্ষার্থী সম্পর্কিত URL
    path('students/', include('students.urls')),
    
    # ইমেইল সম্পর্কিত URL
    path('emails/', include('emails.urls')),
]

# স্ট্যাটিক এবং মিডিয়া ফাইল সার্ভ করা (ডেভেলপমেন্টে)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
