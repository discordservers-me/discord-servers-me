import os
from decouple import config  # , Csv
# import dj_database_url
# currently at web/ (from web/config/settings.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_c4(y9*5jjw2f@ft^%+(fzjbm-10^0l#w2g#*g==_s@e(949nd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'just-a-test-env.33u8ujvqn8.us-west-2.elasticbeanstalk.com', ]


# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config('SECRET_KEY')

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Application definition

INSTALLED_APPS = [

    'material',
    'paypal.standard.ipn',
    'django_summernote',

    'web.apps.auths',
    'web.apps.giveaways',
    'web.apps.premiums.apps.PremiumsConfig',
    'web.apps.users',
    'web.apps.servers',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # 'django.contrib.postgres',
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
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': "ebdb",
            'USER': "ponpon",
            'PASSWORD': "1234qwer",
            'HOST': "aabc0mq37ljm1r.cdjqprmnnwvl.us-west-2.rds.amazonaws.com",
            'PORT': "5432",
        }
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
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Media (User uploaded) url and root
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Discord Bot settings
# BOT_TOKEN = config('BOT_TOKEN')
# BOT_ID = config('BOT_ID')
# BOT_SECRET = config('BOT_SECRET')
BOT_TOKEN = 'NDg3NzgyNDQ4NzQ3NTExODU1.DoPz5Q.FVPtCJznsnWRhapfntsLYXNIdmo'
BOT_ID = '487782448747511855'
BOT_SECRET = 'rU5CUSB1_pQSgAeHQTAk5dmLZwNphHmc'
BUMP_DURATION = 360


DISCORD_REDIRECT_URI = 'auth:discord_callback'
DISCORD_EMAIL_SCOPE = True
# DISCORD_EASY_LOGIN = config('DISCORD_EASY_LOGIN', default=False, cast=bool)
DISCORD_EASY_LOGIN = False
DISCORD_BOT_INVITE_LINK = 'https://discordapp.com/oauth2/authorize?&client_id=487782448747511855&scope=bot&permissions=1'

# Paypal related settings
# PAYPAL_TEST = config('PAYPAL_TEST', default=False, cast=bool)
# PAYPAL_EMAIL_ACCOUNT = config('PAYPAL_EMAIL_ACCOUNT')
PAYPAL_TEST = True
PAYPAL_EMAIL_ACCOUNT = 'trantinan2512-facilitator@gmail.com'

# Discord redirect
# DISCORD_TAIL_URL = config('DISCORD_TAIL_URL', default='dsl')
# DISCORD_INVITE_LINK = config('DISCORD_INVITE_LINK', default='https://discord.gg/tm6GqP4')
DISCORD_TAIL_URL = 'dsl'
DISCORD_INVITE_LINK = 'https://discord.gg/tm6GqP4'
