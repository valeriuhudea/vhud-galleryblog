import os
import environ

import django_heroku

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)
env = environ.Env()

#SECRET_KEY = env.str('SECRET_KEY', default='=zldq$-_=m2@yb_xt-d7h6r#&cxp1rg@n@(&_g^w5+)n^ijp&l')
SECRET_KEY = env('SECRET_KEY')

#DEBUG = False
DEBUG = bool(os.environ.get('DEBUG', 'default=True'))


ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1', '*'])
#ALLOWED_HOSTS = ['*']

# Security
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = 'SAMEORIGIN'

INSTALLED_APPS = [
    'gallery',
	'blog',
    'crispy_forms',
	'taggit',
	'active_link',	
    'storages',
    'rest_framework',
	'sorl.thumbnail',
    'rest_framework.authtoken',
    'djoser',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'anitafrancuart.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), location('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',				
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

WSGI_APPLICATION = 'anitafrancuart.wsgi.application'

'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '', #'',
        'USER': '', #'',
        'PASSWORD': '', #'',
        'HOST': '', #'',
        'PORT': '', #'',
        'SSLMODE': 'require',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DATABASE_NAME', location('db.sqlite')),
        'USER': os.environ.get('DATABASE_USER', None),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', None),
        'HOST': os.environ.get('DATABASE_HOST', None),
        'PORT': os.environ.get('DATABASE_PORT', None),
		'SSLMODE': 'require',
        'ATOMIC_REQUESTS': True
    }
}

# Gmail setup

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''

EMAIL_HOST_USER = env('EMAIL_HOST_USER')#''
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')#''

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'anitafrancuartzld.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'MYAPP': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'anitafrancuart/static'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


### Local Settings only ###
#TEST_LOCAL = False
#
#if TEST_LOCAL:
#    MEDIA_URL = '/media/'
#    #MEDIA_ROOT = 'media'
#    MEDIA_ROOT = location('media')
#    STATIC_URL = '/static/'
#    STATIC_ROOT = location('staticfiles')
#    STATICFILES_DIRS = (location('static'),)
	
### AWS S3 Storage for static and media ###
#else:
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY', None)
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME', None)
AWS_S3_REGION_NAME = os.environ.get('AWS_REGION', None)

# Tell the S3 custom domain to use to serve static files 
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_DEFAULT_ACL = None #

AWS_S3_ENDPOINT_URL = 'https://s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {
'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
'CacheControl': 'max-age=94608000',
}
AWS_LOCATION = 'static'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MEDIA_URL = '/media/'
MEDIA_ROOT = 'http://afart-static.s3.amazonaws.com/'
MEDIAFILES_LOCATION = 'media'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

django_heroku.settings(locals())
