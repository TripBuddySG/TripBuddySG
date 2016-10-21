from django.conf.urls import include,url
from django.contrib import admin
from django.conf.urls.static import static
import os
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('TripBuddy.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)