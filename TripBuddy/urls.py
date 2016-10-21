from django.conf.urls import url
import os

from . import views

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

app_name = 'tripbuddy'
urlpatterns = [
    url(r'^$', view = views.IndexView, name='index'),
    url(r'^about-us/$', views.AboutUsView.as_view(), name = 'about-us'),
    url(r'^why-host/$', views.WhyHostView.as_view(), name = 'why-host'),
    url(r'^legal/$', views.LegalView.as_view(), name = 'legal'),
    url(r'^(?P<trip_id>[0-9]+)/trip/$', view= views.TripView, name='trip'),
    url(r'^feedback/$', view = views.FeedbackView, name = 'feedback'),
    url(r'^testimonials/$', views.TestimonialsView.as_view(), name = 'testimonials'),
    url(r'^view-all-trips/$', view=views.ViewAllTripsView, name = 'view-all-trips'),
    url(r'^new-trip/$', view = views.NewTripView, name = 'new-trip'),
    url(r'^sign-in/$', view = views.SignInView, name = 'sign-in'),
    url(r'^host-profile/$', view = views.HostProfileView, name = 'host-profile'),
    url(r'^register-host/$', view = views.RegisterHostView, name = 'register-host'),
    url(r'^view-all-hosts/$', view = views.ViewAllHostsView, name = 'view-all-hosts'),
    url(r'^host-trips/$', view = views.HostTripsView, name = 'host-trips'),
    ]