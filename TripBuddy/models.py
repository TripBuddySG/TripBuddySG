#TODO: Reviews and Ratings for trips, hosts and users.

'''
This python script describes all the models used in the website
'''

#imports
import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
import os


@python_2_unicode_compatible
class Theme(models.Model):
    
    '''
    Represents a general category of trips
    '''
    
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    
    
@python_2_unicode_compatible
class Trip(models.Model):
    
    '''
    Represents a trip
    '''
    
    #Relationships
    host = models.ForeignKey(User, related_name = 'Host', default = "", on_delete = models.CASCADE)
    custs = models.ManyToManyField(User, default = '', related_name = 'Customers')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, default = '')
    
    #General
    title = models.CharField(max_length=200, null = True)
    tagline = models.TextField(null = True)
    overview = models.TextField(null=True)
    picture = models.ImageField(upload_to='trips')
    itinerary = models.TextField(null=True)
    date = models.DateField(null=True, help_text = 'Date of the Trip')
    startTime = models.TimeField(null=True, help_text= 'Start time of trip')
    endTime = models.TimeField(null=True, help_text = 'End time of trip')
    location = models.CharField(max_length = 200, null=True)
    minGroupSize = models.PositiveIntegerField(null = True, default = 0)
    maxGroupSize = models.PositiveIntegerField(null = True, blank = True)
    price = models.FloatField(null=True)
    itemsList = ArrayField(models.TextField(blank=True), null = True, size = 10)
    includes = ArrayField(models.TextField(blank=True), null = True, size = 10)
    excludes = ArrayField(models.TextField(blank=True), null = True, size = 10)
    transportation = ArrayField(models.TextField(blank=True), size = 20, null = True)
    
    class Meta:
        permissions = (
            ('add_trips','Can add trips to the database'),
            ('delete_trips','Can delete trips from the database')
        )
        
    def __str__(self):
        return self.title
    
    
@python_2_unicode_compatible
class HostDetail(models.Model):
    
    '''
    Details about the host
    '''
    
    #Relationships
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    #General
    tagline = models.TextField(null = True)
    description = models.TextField(null = True)
    university = models.CharField(null = True, max_length = 100)
    course = models.CharField(null=True, max_length = 200)
    year = models.PositiveIntegerField(null=True, default = 0)
    email = models.CharField(null=True, max_length = 100)
    matricId = models.CharField(null=True, max_length = 20)
    school = models.CharField(null = True, max_length = 100)
    rating = models.PositiveIntegerField(null=True, default = 3)
    
    #Bank Details
    account_number = models.CharField(null=True, max_length = 40) 
    account_holder_name = models.CharField(null = True, max_length = 60)
    
    def __str__(self):
        return self.user.username
    
    
@python_2_unicode_compatible
class Feedback(models.Model):
    
    '''
    To accept and read feedback from the users
    '''
    
    email = models.CharField(null = True, max_length = 50)
    name = models.CharField(null = True, max_length = 50)
    feedback = models.TextField(null =True)
    
    def __str__(self):
        return self.name

    
@python_2_unicode_compatible
class CustomUser(models.Model):
    
    '''
    Extension of the user model
    '''
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    new = models.BooleanField(default = True)
    profilePic = models.URLField(default = 'http://www.adtechnology.co.uk/images/UGM-default-user.png')
    link = models.URLField(default ='https://www.facebook.com/')
    
    def __str__(self):
        return self.user.username
    
    
@python_2_unicode_compatible
class Transaction(models.Model):
    
    '''
    Stores details of all transactions
    '''
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_title = models.CharField(max_length=200, null =True)
    txnid = models.CharField(max_length =200, null = True)
    timestamp = models.DateTimeField(null = True)
    paid = models.BooleanField(default= True)
    
    def __str__(self):
        return self.user.username
    
    
@python_2_unicode_compatible
class Newsletter(models.Model):
    
    '''
    To send out newsletter's to the customers
    '''
    
    email = models.CharField(null = True, max_length = 50)
    name = models.CharField(null = True, max_length = 50)
    
    def __str__(self):
        return self.name
    
    
@python_2_unicode_compatible
class Testimonial(models.Model):
    
    '''
    Stores testimonials from selected participants
    '''
    
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    testimonial = models.TextField(null = True)
    def __str__(self):
        return self.user.username