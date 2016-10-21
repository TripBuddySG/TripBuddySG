#TODO: View for newsletters
#TODO: Review and rating system

'''
Views used in the app
'''

#Django Library Imports
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

#Model Imports
from .models import Theme, Trip, HostDetail, Feedback, Transaction, Testimonial
from . import tasks

from random import randint
from datetime import date, timedelta, time, datetime

#Stripe payment engine
import stripe

#Generic List Views

#About Us Page | Template = about-us.html
class AboutUsView(generic.ListView):
    
    '''
    Static page describing the company and its co-founders
    '''
    
    template_name = 'about-us.html'

    def get_queryset(self):
        return

#Why Host Page | Template = why-host.html
class WhyHostView(generic.ListView):
    
    '''
    Static page explaining the benefits of hosting a trip.
    '''
    
    template_name = 'why-host.html'
    
    def get_queryset(self):
        return

#Legal Page | Template = legal.html
class LegalView(generic.ListView):
    
    '''
    Static page detailing our privacy policy and licenses
    '''
    
    template_name = 'legal.html'
    
    def get_queryset(self):
        return
    
#Testimonials Page | Template = testimonials.html
class TestimonialsView(generic.ListView):
    
    '''
    Page showing testimonials from various customers
    '''
    
    template_name = 'testimonials.html'
    context_object_name = 'testimonials'
    
    def get_queryset(self):
        return Testimonial.objects.all()[:6]
    
#Non-generic Views    
#Index page | Template Name = index.html
def IndexView(request):
    
    '''
    View for the index page with contexts of trips, themes and hosts passed.
    '''
    
    context = {}
    context['emailModal'] = False
    
    if request.user.is_authenticated():
        
        if request.method == 'POST':
            request.user.email = request.POST.get('email')
            request.user.save()
            send_mail(
                "Welcome to TripBuddySG", 
                "Hi " + request.user.first_name + 
                ",\n\nMy name is Stacy, the TripBuddy Assistant. \
                I would like to warmly welcome you to Singapore.\
                When we say warmly, we mean it. It is summer all \
                year round here in Singapore! But here is an insider \
                trick - bring a jacket when you go for your classes. \
                The temperature indoors can be quite chilly in most of \
                the academic buildings. \
                \n\nAnyway, I would like to personally thank you for signing\
                up on TripBuddy.SG. We will keep you posted when we find a\
                trip you might like. Meanwhile, feel free to ask us if you\
                have any other random questions you about Singapore. You can\
                 tweet it at us or post it on our Facebook page!\
                \n\nBest Regards, \
                \nStacy\
                \nTripBuddy Assistant", "no-reply@tripbuddy.sg", [ request.user.email ] )
            
        elif request.user.customuser.new == True:
            context['emailModal'] = True
            request.user.customuser.new = False
            request.user.customuser.save()
            send_mail(
                "Welcome to TripBuddySG", 
                "Hi " + request.user.first_name + 
                ",\n\nMy name is Stacy, the TripBuddy Assistant. \
                I would like to warmly welcome you to Singapore.\
                When we say warmly, we mean it. It is summer all \
                year round here in Singapore! But here is an insider \
                trick - bring a jacket when you go for your classes. \
                The temperature indoors can be quite chilly in most of \
                the academic buildings. \
                \n\nAnyway, I would like to personally thank you for signing\
                up on TripBuddy.SG. We will keep you posted when we find a\
                trip you might like. Meanwhile, feel free to ask us if you\
                have any other random questions you about Singapore. You can\
                 tweet it at us or post it on our Facebook page!\
                \n\nBest Regards, \
                \nStacy\
                \nTripBuddy Assistant", "no-reply@tripbuddy.sg", [ request.user.email ] )
        
    context['trips'] = Trip.objects.all().filter( date__gte = date.today() ).order_by('date')[:3]

    context['themes'] = Theme.objects.order_by('title')
        
    group = Group.objects.get_or_create(name='Hosts')
    
    users = User.objects.filter(groups__name ='Hosts').order_by('?')[:3]
    
    context['users'] = users

    return render(request,'index.html',context) 

#Trip Page | Template = trip.html     
def TripView(request, trip_id):
    '''
    Details of a trip.
    '''

    if request.method == 'POST':
        trip = Trip.objects.get(id = trip_id)
        trip.custs.add(request.user)
        trip.save()

        #NOTE: Change key before deployment
        stripe.api_key = "sk_test_ZcwaoPNTeNpxJTF9htVGajTN"

        token = request.POST['stripeToken']

        transaction = Transaction(user = request.user, 
            trip_title = trip.title, 
            timestamp = datetime.now(), paid = False)

        try:
            charge = stripe.Charge.create(
              amount=int(trip.price * 100), 
              currency="sgd",
              source=token,
              description=trip.title + " " + request.user.get_full_name()
              )
            transaction.paid = True
            transaction.txnid = charge.id
        except stripe.error.CardError as e:
            transaction.paid = False
            transaction.txnid = charge.id

        transaction.save()


        #TODO: Add email templates
        '''
        send_mail("Happy Triping", 
                  "Hi " + request.user.first_name + ",\n\nYou just joined a trip.", 
                  "no-reply@tripbuddy.sg", [ request.user.email ])
        send_mail("Happy Triping", 
                  "Hi " + request.user.first_name + ",\n\n" + 
                  request.user.first_name+" just joined your trip!", 
                  "no-reply@tripbuddy.sg", [ trip.host.hostdetail.email, trip.host.email ])
        '''
        
    trip = Trip.objects.get(id=trip_id)
    
    time = False
    
    oneDayBefore = False
    
    if ( date.today() == trip.date - timedelta(days=1)):
        oneDayBefore = True
        
    tripTime = datetime(year = datetime.now().year, 
                        month = datetime.now().month, 
                        day = datetime.now().day, 
                        hour=trip.startTime.hour, 
                        minute = trip.startTime.minute, 
                        second=trip.startTime.second)
    
    currentTime = datetime.now()
    
    if ( date.today() == trip.date ):
        if( tripTime - currentTime >  timedelta(hours=8)):
            time = True
    
    context = {"trip":trip, 'time':time, 'oneDayBefore':oneDayBefore, 'price_in_cents':trip.price*100}
    
    return render(request,'trip.html',context)
    
#Sign-in page | template = sign-in.html
def SignInView(request):
    
    '''
    View to render the sign-in page
    '''
    if(request.method == 'GET'):
        if not request.GET.get('next'):
            if request.user.is_authenticated():
                return redirect('tripbuddy:index')
            if 'HTTP_REFERER' in request.META:
                return render(request,'sign-in.html', {'link': request.META['HTTP_REFERER']})
            else:
                return render(request,'sign-in.html')
        return redirect(request.GET.get('next'))
    
#Feedback Page | Template = feedback.html
def FeedbackView(request):
    
    '''
    Page that gets customer feedback through a form and handles it
    '''
    
    if (request.method == "POST"):
        
        name = request.POST.get("name")
        from_email = request.POST.get("email")
        message = name + " - " + request.POST.get("feedback")
        subject = "Feedback from " + request.user.username
        feedback = Feedback(name = name, email = from_email, feedback = message)
        feedback.save()
        
        if subject and message and from_email:
            send_mail(subject, message, 'no-reply@tripbuddy.sg', ['contact@tripbuddy.sg'])
        else:
            return render(request, 'feedback.html')
        
        return redirect('tripbuddy:index')
    
    return render(request, "feedback.html")

#View all hosts page | Template = view-all-hosts.html
def ViewAllHostsView(request):
    
    '''
    Page that displays details of all hosts
    '''
    
    if(request.method == "GET"):
        universityGet = request.GET.get('university')
        schoolGet = request.GET.get('school')
        
        schools = {'':[],'Any University':[], 
                   'Nanyang Technological University': ['Nanyang Business School', 
                                                        'School of Chemical and Biomedical Engineering', 
                                                        'School of Civil and Environmental Engineering', 
                                                        'School of Computer Engineering',
                                                        'School of Electrical and Electronic Engineering', 
                                                        'School of Materials Science and Engineering', 
                                                        'School of Mechanical and Aerospace Engineering', 
                                                        'School of Art, Design and Media', 
                                                        'School of Humanities and Social Sciences', 
                                                        'Wee Kim Wee School of Communication and Information',
                                                        'School of Biological Sciences', 
                                                        'School of Physical and Mathematical Sciences', 
                                                        'Lee Kong Chian School of Medicine'], 
                   'National University of Singapore': ['Faculty of Arts & Social Sciences',
                                                        'NUS Business School', 
                                                        'School of Computing',
                                                        'Faculty of Dentistry', 
                                                        'School of Design & Environment', 
                                                        'Faculty of Engineering',
                                                        'Yong Loo Lin School of Medicine', 
                                                        'Faculty of Science', 
                                                        'Lee Kuan Yew School of Public Policy',
                                                        'Faculty of Law'],
                   'Singapore Management University':  ['School of Accountancy', 
                                                        'Lee Kong Chian School of Business', 
                                                        'School of Economics',
                                                        'School of Information Systems', 
                                                        'School of Law', 'School of Social Sciences']}
        
        hosttrips = {}
        
        for hostdetail in HostDetail.objects.all():
            hosttrips[ hostdetail.user.username ] = Trip.objects.all().filter(host = hostdetail.user)[:3]
                
        if not universityGet:
            return render(request, 'view-all-hosts.html', 
                  { 'users': HostDetail.objects.all(),
                    'trips': hosttrips,
                    'uniNext':'Any University',
                    'schoolNext':'Any School',
                    'schools':schools['']  })
        if universityGet == 'Any University':
            return render(request, 'view-all-hosts.html', 
                  { 'users': HostDetail.objects.all(),
                    'trips':hosttrips,
                    'uniNext':universityGet,
                    'schoolNext':'Any School',
                    'schools':schools[''] })
        elif schoolGet == 'Any School':
            hostdetail = HostDetail.objects.all().filter(university = universityGet)
            return render(request, 'view-all-hosts.html', 
                  { 'users': hostdetail, 
                    'trips':hosttrips,
                    'uniNext':universityGet,
                    'schoolNext':schoolGet,
                    'schools':schools[universityGet] })
        else:
            hostdetail = HostDetail.objects.all().filter(university = universityGet, school = schoolGet)
            return render(request, 'view-all-hosts.html', 
                   { 'users': hostdetail, 
                     'trips':hosttrips,
                     'uniNext':universityGet,
                     'schoolNext':schoolGet,
                     'schools':schools[universityGet] })

#Host Detail page | Template = register.html
@login_required
def RegisterHostView(request):
    '''
    Page that signs up any host
    '''
    if(request.method == 'POST'):
        
        uniPost = request.POST.get("university")
        schoolPost = request.POST.get("school")
        coursePost = request.POST.get("course")
        descrPost = request.POST.get("descr")
        yearPost = request.POST.get("study_year")
        emailPost = request.POST.get("univ_email")
        matricPost = request.POST.get("univ_matric")
        taglinePost = request.POST.get("tagline")
        
        host = HostDetail(university = uniPost, 
                          school = schoolPost, 
                          year = yearPost, 
                          email = emailPost, 
                          tagline = taglinePost, 
                          matricId = matricPost, 
                          course = coursePost, 
                          description = descrPost, 
                          user = request.user)
        host.save()
        
        send_mail("Welcome to TripBuddySG", 
                  "Hi " + request.user.first_name + 
                  ",\n\nMy name is Alan, the TripBuddy Assistant. We would like to personally welcome you to the guild of the great TripBuddy Hosts! Congratulations on taking the first step to becoming a full-time awesome person! We hope that you are excited because this is going to be a life changing experience. Nervous? Don’t be! All the resources you need to become a successful host are on our website.\
                    \n\nWe will see you soon. And welcome to the TripBuddy family!\
                    \n\nBest Regards,\
                    \nAlan\
                    \nTripBuddy Assistant", "no-reply@tripbuddy.sg",[host.email])
        
        if Group.objects.count() == 0 :
            group = Group.objects.create(name='Hosts')
            group.permissions = [Permission.objects.get(name = 'add_trips'), 
                                 Permission.objects.get(name= 'delete_trips')]
        else:
            group = Group.objects.get(name='Hosts')
        group.user_set.add(request.user)
        group.save()
        
        return redirect('tripbuddy:index')    
    return render(request, 'register.html')

#Host Profile page | template = host-profile.html
def HostProfileView(request):
    '''
    Page that allows host to view his details and edit them
    '''
    if not request.user.is_authenticated():
        return redirect('tripbuddy:sign-in')
    
    if(request.method == 'POST'):
        flag =0
        host = HostDetail.objects.get(user=request.user)
        
        uniPost = request.POST.get("university")
        schoolPost = request.POST.get("school")
        coursePost = request.POST.get("course")
        descrPost = request.POST.get("descr")
        yearPost = request.POST.get("study_year")
        emailPost = request.POST.get("univ_email")
        matricPost = request.POST.get("univ_matric")
        taglinePost = request.POST.get("tagline")
        
        if(host.university != uniPost):
            host.university = uniPost
            flag=1
        if(host.school != schoolPost):
            host.school = schoolPost
            flag=1
        if(host.course != coursePost):
            host.course = coursePost
            flag=1
        if(host.description != descrPost):
            host.description = descrPost
            flag=1
        if(host.year != yearPost):
            host.year = yearPost
            flag=1
        if(host.email != emailPost):
            host.email = emailPost
            flag=1
        if(host.matricId != matricPost):
            host.matricId = matricPost
            flag=1
        if(host.tagline != taglinePost):
            host.tagline = taglinePost
            flag=1
        if flag ==1:
            host.save()

        return redirect('tripbuddy:index')
    
    context = {}
    if request.user.hostdetail.university == 'Nanyang Technological University':
        context['schools'] = ['Nanyang Business School', 
                              'School of Chemical and Biomedical Engineering', 
                              'School of Civil and Environmental Engineering', 
                              'School of Computer Engineering', 
                              'School of Electrical and Electronic Engineering', 
                              'School of Materials Science and Engineering', 
                              'School of Mechanical and Aerospace Engineering', 
                              'School of Art, Design and Media', 
                              'School of Humanities and Social Sciences', 
                              'Wee Kim Wee School of Communication and Information', 
                              'School of Biological Sciences', 
                              'School of Physical and Mathematical Sciences', 
                              'Lee Kong Chian School of Medicine']
        
    elif request.user.hostdetail.university == 'National University of Singapore':
        context['schools'] = ['Faculty of Arts & Social Sciences',
                              'NUS Business School', 
                              'School of Computing', 
                              'Faculty of Dentistry', 
                              'School of Design & Environment', 
                              'Faculty of Engineering', 
                              'Yong Loo Lin School of Medicine', 
                              'Faculty of Science', 
                              'Lee Kuan Yew School of Public Policy', 
                              'Faculty of Law']
    else:
        context['schools'] = ['School of Accountancy', 
                              'Lee Kong Chian School of Business', 
                              'School of Economics', 
                              'School of Information Systems', 
                              'School of Law', 
                              'School of Social Sciences']
        
    return render(request,'host-profile.html',context)

#Trip form page | template = new-trip.html
def NewTripView(request):
    '''
    Page that allows host to register a new trip.
    '''
    
    if not request.user.is_authenticated():
        return redirect('tripbuddy:sign-in')
    
    if not request.user.groups.filter(name='Hosts').exists():
        return redirect('tripbuddy:register-host')
    
    if(request.method == "POST"):
        
        titlePost = request.POST.get('title')
        taglinePost = request.POST.get('tagline')
        overviewPost = request.POST.get('overview')
        itineraryPost = request.POST.get('itinerary')
        datePost = request.POST.get('date')
        start_timePost = request.POST.get('time_start')
        end_timePost = request.POST.get('time_end')
        locationPost = request.POST.get('location')
        min_groupPost = request.POST.get('min_group')
        max_groupPost = request.POST.get('max_group')
        pricePost = request.POST.get('price')
        itemsListPost = request.POST.getlist('items')
        includesPost = request.POST.getlist('includes')
        excludesPost = request.POST.getlist('excludes')
        transport_walk = request.POST.get('transport_walk')
        transport_cab = request.POST.get('transport_cab')
        transport_public =request.POST.get('transport_public')
        transport_car =request.POST.get('transport_car')
        transport_bus = request.POST.get('transport_bus')
        themePost = request.POST.get('theme','Adventure')

        transportationArr = []

        if(transport_walk):
            transportationArr.append(transport_walk)
        if(transport_cab):
            transportationArr.append(transport_cab)
        if(transport_public):
            transportationArr.append(transport_public)
        if(transport_car):
            transportationArr.append(transport_car)
        if(transport_bus):
            transportationArr.append(transport_bus)


        trip = Trip(picture=request.FILES.get('pic'),
                    tagline = taglinePost,
                    title = titlePost, overview = overviewPost, 
                    location =locationPost, 
                    itinerary = itineraryPost,date = datePost,
                    startTime = start_timePost,
                    endTime = end_timePost,
                    minGroupSize = min_groupPost,
                    maxGroupSize = max_groupPost,
                    price = pricePost,
                    itemsList = itemsListPost,
                    includes = includesPost,
                    excludes = excludesPost,
                    transportation = transportationArr,
                    theme= Theme.objects.all().get(title=themePost),
                    host = request.user)
        trip.save()
            
        send_mail("Congratulations", 
                  "Hello again " + request.user.first_name + 
                  ",\n\nMy name is Alan, the TripBuddy Assistant. Warm greetings from TripBuddy! Thank you for hosting your trip " + trip.title +". We will updating you along your hosting journey. Please do email us at contact@tripbuddy.sg if you have any questions.\
                    \n\nWe look forward to the trip!\
                    \n\nBest Regards, \
                    \nAlan\
                    \nTripBuddy Assistant ", 
                  "no-reply@tripbuddy.sg",
                  [trip.host.hostdetail.email, trip.host.email])
           
        # Start background services
        # NOTE: Remove if using mailchimp
        dateTrip =  datetime.strptime(datePost, "%Y-%m-%d").date()
        timeTrip = datetime.strptime(start_timePost,"%H:%M").time()
        dateTime = datetime(dateTrip.year, dateTrip.month, dateTrip.day, timeTrip.hour, timeTrip.minute)
        offset = datetime.now() - datetime.utcnow()
        utcDateTime = dateTime - offset 

        #tasks.mail_custs.apply_async(args=["Your trip is tomorrow", 
        #                             "You have signed up for "+trip.title+"tomorrow", "no-reply@tripbuddy.sg", 
        #                             trip.id], eta = utcDateTime - timedelta(days=1))
        #tasks.mail_custs.apply_async(args=["Your trip is tomorrow",
        #                             "You have signed up for "+trip.title+"tomorrow",
        #                             "no-reply@tripbuddy.sg",trip.id],eta = utcDateTime)
        #tasks.mail_host.apply_async(args=["Your trip is tomorrow",
        #                            "You have signed up for "+trip.title+"tomorrow",
        #                            "no-reply@tripbuddy.sg",trip.id],eta = utcDateTime - timedelta(days=1))
        #tasks.mail_host.apply_async(args=["Your trip is tomorrow",
        #                            "You have signed up for "+trip.title+"tomorrow",
        #                           "no-reply@tripbuddy.sg",trip.id], eta = utcDateTime)

        return render(request,'new-trip-success.html',{'trip':trip})
        
    return render(request,'new-trip.html',{'themes':Theme.objects.all()})


#View all trips page | template = view-all-trips.html
def ViewAllTripsView(request):
    '''
    Page that shows the details of all the trips
    '''
    
    #Get Parameters
    themeGet = request.GET.get('theme', 'Any Theme')
    priceGet = request.GET.get('price', 'Any Price')
    dateGet = request.GET.get('date', 'Any Date')
    
    #Fixing the price ranges
    price_low = 2.2250738585072014e-308  #Minimum allowed float value
    price_high = 1.7976931348623157e+308 #Maximum allowed float value
    
    if priceGet == 'x<20': 
        price_high = 20
    elif priceGet == '20<x<50':
        price_low = 20
        price_high = 50
    elif priceGet == '50<x<80':
        price_low = 50
        price_high = 80
    else:
        price_low = 80
        
    #Date Array for one week
    d = date.today()
    date_arr = []
    for i in range(0,7):
        date_arr.append(d+timedelta(days=i))
        
    #Statements for computing correct context
    if not Trip.objects.all():
        return render(request,'view-all-trips.html', 
                  {'trips':Trip.objects.all().filter(date__gte = d),
                   'themes':Theme.objects.all().filter().order_by('title'),
                   'themeNext':themeGet,
                   'priceNext':priceGet,'dateNext':dateGet
                  ,'date_arr':date_arr})
    if(themeGet == 'Any Theme' and priceGet == 'Any Price' and dateGet == 'Any Date'):
        return render(request, 'view-all-trips.html', 
                {'trips':Trip.objects.all().filter(date__gte = d),
                 'themes':Theme.objects.all().order_by('title'),
                 'themeNext':themeGet,
                 'priceNext':priceGet,
                 'dateNext':dateGet,
                 'date_arr':date_arr})
    
    elif (themeGet == 'Any Theme'):
        
        if(priceGet == 'Any Price'):
            return render(request,'view-all-trips.html',
                          { 'trips' : Trip.objects.all().filter(date=dateGet),
                            'themes' : Theme.objects.all().order_by('title'),'themeNext':themeGet,
                            'priceNext' : priceGet, 
                           'dateNext' : dateGet, 
                           'date_arr' : date_arr})
        
        elif(dateGet == 'Any Date'):
            return render(request,'view-all-trips.html', 
                          {'trips':Trip.objects.all().filter(price__lte = price_high, price__gte = price_low, date__gte = d),
                           'themes':Theme.objects.all().order_by('title'),
                           'themeNext':themeGet,'priceNext':priceGet,
                           'dateNext':dateGet,'date_arr':date_arr})
        
        else:
            return render(request,'view-all-trips.html', 
                          {'trips':Trip.objects.all().filter(price__lte = price_high, price__gte = price_low, date = dateGet),
                           'themes':Theme.objects.all().order_by('title'),
                           'themeNext':themeGet,
                           'priceNext':priceGet,
                           'dateNext':dateGet,
                           'date_arr':date_arr})
        
    elif (priceGet == 'Any Price'):
        
        if (dateGet == 'Any Date'):
            return render(request,'view-all-trips.html', 
                          {'trips':Trip.objects.all().filter(theme = Theme.objects.get(title=themeGet), date__gte = d),
                           'themes':Theme.objects.all().order_by('title'),
                           'themeNext':themeGet,
                           'priceNext':priceGet,
                           'dateNext':dateGet,
                           'date_arr':date_arr})
        
        else:
            return render(request,'view-all-trips.html', 
                          {'trips':Trip.objects.all().filter(theme = Theme.objects.get(title = themeGet), date = dateGet),
                           'themes':Theme.objects.all().order_by('title'),
                           'themeNext':themeGet,
                           'priceNext':priceGet,
                           'dateNext':dateGet,
                           'date_arr':date_arr})
        
    elif (dateGet == 'Any Date'):
        return render(request,'view-all-trips.html', 
                      {'trips':Trip.objects.all().filter(price__lte = price_high, 
                        price__gte = price_low, 
                        theme = Theme.objects.get(title=themeGet), 
                        date__gte = d),
                       'themes':Theme.objects.all().order_by('title'),
                       'themeNext':themeGet,
                       'priceNext':priceGet,
                       'dateNext':dateGet,
                       'date_arr':date_arr})
    
    return render(request,'view-all-trips.html', 
                  {'trips':Trip.objects.all().filter(price__lte = price_high, 
                    price__gte = price_low, theme = Theme.objects.get(title=themeGet), 
                    date=dateGet),
                   'themes':Theme.objects.all().order_by('title'),
                   'themeNext':themeGet,
                   'priceNext':priceGet,
                   'dateNext':dateGet,
                   'date_arr':date_arr})

#Host trips page | template = host-trips.html.html
def HostTripsView(request):
    '''
    Page that shows the trips hosted by the user
    '''

    if not request.user.is_authenticated():
        return redirect('tripbuddy:sign-in')
    
    if not request.user.groups.filter(name='Hosts').exists():
        return redirect('tripbuddy:register-host')
    
    #Get Parameters
    themeGet = request.GET.get('theme', 'Any Theme')
    priceGet = request.GET.get('price', 'Any Price')
    dateGet = request.GET.get('date', 'Any Date')
    
    #Fixing the price ranges
    price_low = 2.2250738585072014e-308  #Minimum allowed float value
    price_high = 1.7976931348623157e+308 #Maximum allowed float value
    if priceGet == 'x<20': 
        price_high = 20
    elif priceGet == '20<x<50':
        price_low = 20
        price_high = 50
    elif priceGet == '50<x<80':
        price_low = 50
        price_high = 80
    else:
        price_low = 80
        
    #Date Array for one week
    d = date.today()
    date_arr = []
    for i in range(0,7):
        date_arr.append(d+timedelta(days=i))
        
    #Statements for computing correct context
    if not Trip.objects.all().filter(host = request.user):
        return render(request, 'host-trips.html',
                    {'themeNext':themeGet,
                   'priceNext':priceGet,'dateNext':dateGet,
                   'hostTrips':False })

    if not Trip.objects.all():
        return render(request,'host-trips.html', 
                  {'trips':Trip.objects.all().filter(date__gte = d, host=request.user),
                   'themes':Theme.objects.all().filter().order_by('title'),
                   'themeNext':themeGet,
                   'priceNext':priceGet,'dateNext':dateGet
                  ,'date_arr':date_arr, 'hostTrips':True})
    if(themeGet == 'Any Theme' and priceGet == 'Any Price' and dateGet == 'Any Date'):
        return render(request, 'host-trips.html', 
                {'trips':Trip.objects.all().filter(date__gte = d, host=request.user),
                 'themes':Theme.objects.all().order_by('title'),
                 'themeNext':themeGet,
                 'priceNext':priceGet,
                 'dateNext':dateGet,
                 'date_arr':date_arr, 'hostTrips':True})
    
    elif (themeGet == 'Any Theme'):
        
        if(priceGet == 'Any Price'):
            return render(request,'host-trips.html',
                          { 'trips' : Trip.objects.all().filter(date=dateGet, host=request.user),
                            'themes' : Theme.objects.all().order_by('title'),'themeNext':themeGet,
                            'priceNext' : priceGet, 
                           'dateNext' : dateGet, 
                           'date_arr' : date_arr, 'hostTrips':True})
        
        elif(dateGet == 'Any Date'):
            return render(request,'host-trips.html', 
                          {'trips':Trip.objects.all().filter(host=request.user, 
                            price__lte = price_high, price__gte = price_low, date__gte = d),
                           'themes':Theme.objects.all().order_by('title'),
                           'themeNext':themeGet,'priceNext':priceGet,
                           'dateNext':dateGet,'date_arr':date_arr, 'hostTrips':True})
        
        else:
            return render(request,'host-trips.html', 
                          {'trips':Trip.objects.all().filter(host=request.user, 
                            price__lte = price_high, price__gte = price_low, date = dateGet),
                           'themes':Theme.objects.all().order_by('title'),
                           'themeNext':themeGet,
                           'priceNext':priceGet,
                           'dateNext':dateGet,
                           'date_arr':date_arr, 'hostTrips':True})
        
    elif (priceGet == 'Any Price'):
        
        if (dateGet == 'Any Date'):
            return render(request,'host-trips.html', 
                          {'trips':Trip.objects.all().filter(host=request.user, 
                            theme = Theme.objects.get(title=themeGet), date__gte = d),
                           'themes':Theme.objects.all().order_by('title'),
                           'themeNext':themeGet,
                           'priceNext':priceGet,
                           'dateNext':dateGet,
                           'date_arr':date_arr, 'hostTrips':True})
        
        else:
            return render(request,'host-trips.html', 
                          {'trips':Trip.objects.all().filter(host=request.user, 
                            theme = Theme.objects.get(title = themeGet), date = dateGet),
                           'themes':Theme.objects.all().order_by('title'),
                           'themeNext':themeGet,
                           'priceNext':priceGet,
                           'dateNext':dateGet,
                           'date_arr':date_arr, 'hostTrips':True})
        
    elif (dateGet == 'Any Date'):
        return render(request,'host-trips.html', 
                      {'trips':Trip.objects.all().filter(host=request.user, 
                        price__lte = price_high, price__gte = price_low, 
                        theme = Theme.objects.get(title=themeGet), date__gte = d),
                       'themes':Theme.objects.all().order_by('title'),
                       'themeNext':themeGet,
                       'priceNext':priceGet,
                       'dateNext':dateGet,
                       'date_arr':date_arr, 'hostTrips':True})
    
    return render(request,'host-trips.html', 
                  {'trips':Trip.objects.all().filter(host=request.user, 
                    price__lte = price_high, price__gte = price_low, 
                    theme = Theme.objects.get(title=themeGet), date=dateGet),
                   'themes':Theme.objects.all().order_by('title'),
                   'themeNext':themeGet,
                   'priceNext':priceGet,
                   'dateNext':dateGet,
                   'date_arr':date_arr, 'hostTrips':True})