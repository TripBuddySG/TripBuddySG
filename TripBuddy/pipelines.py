'''
This script is a custom backend pipeline for the facebook social auth
'''

from requests import request, HTTPError

from .models import CustomUser

from django.contrib.auth.models import User, Group, Permission

from . import views

from django.core.files.base import ContentFile

def save_profile_picture(backend, strategy, details, response, user=None, *args, **kwargs):
    url_large = None
    if backend.name == 'facebook':
        url_large = "http://graph.facebook.com/%s/picture?width=400&height=400"%response['id']
    if backend.name == 'twitter':
        url_large = response.get('profile_image_url', '').replace('_normal','')
    if backend.name == 'google-oauth2':
        url_large = response['image'].get('url')
        ext = url_large.split('.')[-1]
    if url_large: 
        if CustomUser.objects.filter(profilePic = url_large, user=user).count() == 0:
            customuser= CustomUser(profilePic = url_large, user=user, link = response.get('link'), new = True)
            customuser.save()