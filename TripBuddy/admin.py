#imports

#Django Imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

#Model Import
from .models import Theme, Trip,HostDetail,Feedback,CustomUser,Transaction,Testimonial,Newsletter

#Inlines
class TripsInline(admin.TabularInline):
    model = Trip
    extra = 0
    verbose_name_plural = 'trip'

class CustomUserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    
#Admin consoles
class TripsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Theme', {'fields': ['theme']}),
        ('Overview', {'fields': ['overview']}),
        ('Tagline', {'fields':['tagline']}),
        ('Picture', {'fields': ['picture']}),
        ('Location', {'fields': ['location']}),
        ('Date of Trip', {'fields': ['date']}),
        ('Start Time', {'fields': ['startTime']}),
        ('End Time', {'fields': ['endTime']}),
        ('Includes', {'fields': ['includes']}),
        ('Excludes', {'fields': ['excludes']}),
        ('MinGroupSize', {'fields': ['minGroupSize']}),
        ('MaxGroupSize', {'fields': ['maxGroupSize']}),
        ('Transportation', {'fields': ['transportation']}),
        ('itinerary', {'fields': ['itinerary']}),
        ('Price', {'fields': ['price']}),
        ('UserHost', {'fields': ['host']}),
        ('UserCust', {'fields': ['custs']}),
    ]


class ThemesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
    ]
    
class HostDetailAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user']}),
        ('University', {'fields': ['university']}),
        ('School', {'fields': ['school']}),
        ('Course', {'fields': ['course']}),
        ('Year', {'fields': ['year']}),
        ('Email', {'fields': ['email']}),
        ('MatricID', {'fields': ['matricId']}),
        ('Tagline', {'fields': ['tagline']}),
        ('Description', {'fields': ['description']}),
    ]
    
class FeedbackAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('email', {'fields': ['email']}),
        ('feedback', {'fields': ['feedback']}),
    ]
    
class TransactionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user']}),
        ('Trip Title', {'fields': ['trip_title']}),
        ('Transaction ID', {'fields': ['txnid']}),
        ('Invoice Number', {'fields': ['invoice']}),
        ('Timestamp', {'fields': ['timestamp']}),
        ('Paid', {'fields': ['paid']}),
    ]
    
class NewsletterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('email', {'fields': ['email']}),
    ]
    
class TestimonialAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user']}),
        ('testimonial', {'fields': ['testimonial']}),
    ]
    
class UserAdmin(BaseUserAdmin):
    inlines = (CustomUserInline, )

#Site Registrations
admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Theme, ThemesAdmin)
admin.site.register(HostDetail, HostDetailAdmin)
admin.site.register(Trip, TripsAdmin)
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Newsletter,NewsletterAdmin)
admin.site.register(Testimonial,TestimonialAdmin)