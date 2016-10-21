import os
import keys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = keys.SECRET_KEY

#NOTE: Remove the following two lines before deployment
DEBUG = True

ALLOWED_HOSTS = ['tripbuddy.xyz','tripbuddy.sg']


INSTALLED_APPS = [
    'TripBuddy.apps.TripBuddyConfig',
    'social.apps.django_app.default',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'TripBuddySG.Middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'TripBuddySG.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

#Authentication Pipelines. See pipelines.py
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email', 
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'TripBuddy.pipelines.save_profile_picture',
)

#Authentication Backends
#FUTURE: Twitter and Google Plus OAuth :'social.backends.google.GoogleOAuth2',   'social.backends.twitter.TwitterOAuth',
AUTHENTICATION_BACKENDS = (
   'social.backends.facebook.FacebookOAuth2',
   'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_FACEBOOK_KEY = keys.SOCIAL_AUTH_FACEBOOK_KEY
SOCIAL_AUTH_FACEBOOK_SECRET = keys.SOCIAL_AUTH_FACEBOOK_SECRET
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'ru_RU',
  'fields': 'id, name, email, age_range,link'
}

WSGI_APPLICATION = 'TripBuddySG.wsgi.application'

#NOTE: Modify database settings according to the server
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'TripBuddySG',
        'USER': 'postgres',
        'PASSWORD': keys.dbpassword,
        'HOST': 'localhost',
        'PORT': '',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/'

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = keys.MEDIA_ROOT

STATIC_ROOT = '/opt/myenv/staticfiles'

#NOTE: Modify to new mail host
#Email Services
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = keys.EMAIL_HOST
EMAIL_HOST_USER = keys.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = keys.EMAIL_HOST_PASSWORD
EMAIL_PORT = keys.EMAIL_PORT
EMAIL_USE_SSL = True

#NOTE: Remove if using mailchimp
#Background services for celery
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
