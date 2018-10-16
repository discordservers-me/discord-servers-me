import os
from decouple import config, Csv
import dj_database_url
# currently at web/ (from web/config/settings.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'django.contrib.postgres',
    'django_summernote',
    'material',
    'paypal.standard.ipn',

    'web.apps.auths',
    'web.apps.core',
    'web.apps.giveaways',
    'web.apps.premiums.apps.PremiumsConfig',
    'web.apps.users',
    'web.apps.servers',
    'web.apps.partner',
    'web.apps.about',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web.config.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'web.config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
if DEBUG is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD'),
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL')
        )
    }


AUTH_USER_MODEL = 'users.User'


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Authentication settings
LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = '/auth/login'

# Static url and root
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Media (User uploaded) url and root
MEDIA_ROOT = os.path.join(BASE_DIR, 'staticfiles/img/media')
MEDIA_URL = '/static/img/media/'

# Discord Bot settings
BOT_TOKEN = config('BOT_TOKEN')
BOT_ID = config('BOT_ID')
BOT_SECRET = config('BOT_SECRET')
BUMP_DURATION = config('BUMP_DURATION', default=360, cast=int)
UPDATE_MANAGERS_DURATION = config('UPDATE_MANAGERS_DURATION', default=600, cast=int)
UPDATE_SERVERS_INFO = config('UPDATE_SERVERS_INFO', default=120, cast=int)


DISCORD_REDIRECT_URI = 'auth:discord_callback'
DISCORD_EMAIL_SCOPE = config('DISCORD_EMAIL_SCOPE', default=False, cast=bool)
DISCORD_EASY_LOGIN = config('DISCORD_EASY_LOGIN', default=False, cast=bool)
DISCORD_BOT_INVITE_LINK = config('DISCORD_BOT_INVITE_LINK')

# Paypal related settings
PAYPAL_TEST = config('PAYPAL_TEST', default=False, cast=bool)
PAYPAL_EMAIL_ACCOUNT = config('PAYPAL_EMAIL_ACCOUNT')
PREMIUM_VIDEO = config('PREMIUM_VIDEO')

# Discord redirect
DISCORD_TAIL_URL = config('DISCORD_TAIL_URL', default='dsl')
DISCORD_INVITE_LINK = config('DISCORD_INVITE_LINK', default='https://discord.gg/tm6GqP4')

# Website Metas
META_DESCRIPTION = config('META_DESCRIPTION', default="Oh this is some meta tag!")
