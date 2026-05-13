from minor.settings import BASE_DIR

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'api',
    'accounts',
]

AUTH_USER_MODEL = 'core.User'

TEMPLATES = [
    {
        
        'DIRS': [
                 BASE_DIR / "static",        # pehla folder
                 BASE_DIR / "templates",    
                 ]
        
    },
]

CSRF_TRUSTED_ORIGINS = [
    
]
    
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static',BASE_DIR / 'templates']  
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# settings.py
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
# Inherit secure cookie behavior from the main project settings (minor/settings.py)
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
