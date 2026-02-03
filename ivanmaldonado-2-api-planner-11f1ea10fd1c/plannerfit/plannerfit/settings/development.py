from plannerfit.settings.common import * 
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'plannerfit', 
        'USER': 'postgres', 
        'PASSWORD': 'PlannerFit2023',
        'HOST': 'db', 
        'PORT': 5432
    }
}
