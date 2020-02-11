# pip install django
# pip install djangorestframework
# pip install djangorestframework-jwt
# pip install django-filter

# popular settings for me
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_jwt',
]

MEDIA_ROOT = os.path.join(BASE_DIR)
MEDIA_URL = '/uploads/'

AUTH_USER_MODEL = 'accounts.CustomUser'
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'accounts.serializers.jwt_response_payload_handler'
}
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    # 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),

    # To set the throttle rates or request limit rate
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/min',  # ,'5/day'
        'user': '1000/day'
    },
}

# corsheaders
# pip install django-cors-headers
MIDDLEWARE = [  # Or MIDDLEWARE_CLASSES on Django < 1.10
    ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]
INSTALLED_APPS = [
    ...
    "corsheaders"
        ...
]
CORS_ORIGIN_ALLOW_ALL = True

# MEDIA URL SETTINGS
# urls.py
from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# settings.py
MEDIA_ROOT = os.path.join(BASE_DIR)
MEDIA_URL = '/api/v1/uploads/'

# Install Swagger
# pip install django-rest-swagger
# urls.py
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='APP Title')

urlpatterns += [
    path(r'api/v1/swagger/', schema_view)
]

# Email Configuration
""" Email Settings """
EMAIL_USE_TLS = True
EMAIL_HOST = get_env_variable("EMAIL_HOST")
EMAIL_HOST_USER = get_env_variable('EMAIL_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_PASSWORD')
EMAIL_PORT = int(get_env_variable('EMAIL_PORT'))
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# get_env_variable
import os
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)












