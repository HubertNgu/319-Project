# Django settings for virtual_deconstruction_hub project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# OS Specific path settings for project
import os
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cs319dennis',                      # Or path to database file if using sqlite3.
        'USER': 'cs319team4',                      # Not used with sqlite3.
        'PASSWORD': 'qwerty',                  # Not used with sqlite3.
        'HOST': '174.7.161.223',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Vancouver'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = 'photo_uploads/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"

MEDIA_URL = '/photos/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
		os.path.join(PROJECT_PATH, 'static_files_dir'),
		)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
		'django.contrib.staticfiles.finders.FileSystemFinder',
		'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
		)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'kmf^mp7umaxeazrlwcmf*8ys2!y+(c6f473#ug&amp;w00iplyxl7&amp;'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
			'django.template.loaders.filesystem.Loader',
			'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
			)

MIDDLEWARE_CLASSES = (
			'django.middleware.common.CommonMiddleware',
			'django.contrib.sessions.middleware.SessionMiddleware',
			'django.middleware.csrf.CsrfViewMiddleware',
			'django.contrib.auth.middleware.AuthenticationMiddleware',
			'django.contrib.messages.middleware.MessageMiddleware',
# Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

ROOT_URLCONF = 'virtual_deconstruction_hub.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'virtual_deconstruction_hub.wsgi.application'


TEMPLATE_DIRS = (
# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
		os.path.join(PROJECT_PATH, 'templates_dir')
		)

TEMPLATE_STRING_IF_INVALID = 'error getting correct variable'

INSTALLED_APPS = (
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.sites',
		'django.contrib.messages',
		'django.contrib.staticfiles',
		'users',
# Uncomment the next line to enable the admin:
		'django.contrib.admin',
# Uncomment the next line to enable admin documentation:
		'django.contrib.admindocs',
		'posts',
		'listings',
		'statistics_generator',
		'survey_system',
		'userprofile',
		'verificationapp',
		'fileupload',
		'postpictures',
                'chart_tools',
                'mailer',
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Host for sending e-mail
EMAIL_HOST = 'smtp.gmail.com'
# Port for sending e-mail
EMAIL_PORT = 587
# Option SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = 'ubccs319team4@gmail.com'
EMAIL_HOST_PASSWORD = '1029384756qpwoeiruty'
EMAIL_USE_TLS = True

RESULTS_PAGE_SIZE = 100

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


