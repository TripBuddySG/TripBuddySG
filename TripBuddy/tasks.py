#NOTE: Remove if using MailChimp
from __future__ import absolute_import

from TripBuddySG.celery import app

from .models import Trip

from django.core.mail import send_mail

@app.task
def mail_custs(subject, message, from_email, i):
    email_list = []  
    for cust in Trip.objects.all().get(id=i).custs.all():
        email_list.append(cust.email)
    send_mail(subject, message, from_email, email_list)
    
@app.task
def mail_host(subject, message, from_email, i):
    send_mail(subject, message, from_email, [Trip.objects.all().get(id=i).host.hostdetail.email,Trip.objects.all().get(id=i).host.email])
    