# display image field django in admin panel
# Not Worked
def headshot_image(self, obj):
    return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
        url=obj.headshot.url, width=obj.headshot.width, height=obj.headshot.height, ))

# Correct
readonly_fields = ["image_tag"]
def image_tag(self, obj):
    from django.utils.html import escape
    return mark_safe(u'<img src="%s" />' % escape(obj.image.url))

image_tag.short_description = 'Image'
image_tag.allow_tags = True


# renaming the uploaded file
import random
import os
def rename_file(inctance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    random_str = ''.join((random.choice(chars)) for x in range(10))
    return 'uploads/cv_files/{random_string}{extension}'.format(basename=base_filename,
                                                                random_string=random_str,
                                                                extension=file_extension)


# change pass restful
# view.py
class ChangePasswordView(UpdateAPIView):
    model = CustomUser
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"status": "Password is Incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                MinimumLengthValidator().validate(serializer.data.get("new_password"))
                CommonPasswordValidator().validate(serializer.data.get("new_password"))
                NumericPasswordValidator().validate(serializer.data.get("new_password"))
            except ValidationError as e:
                return Response({"status": e}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"status": "Success."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# serializers.py
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

# urls.py
path(r'api/v1/change-password/', ChangePasswordView.as_view())



# Django database diagram extention
# requirements
django-extensions==2.2.1
graphviz==0.11.1
pydotplus==2.0.2
pygraphviz==1.5
pyparsing==2.4.2
INSTALLED_APPS = (
    'django_extensions',
)
# dependencis
sudo apt-get install python-dev graphviz libgraphviz-dev pkg-config
# commands
python manage.py graph_models -a -o myapp_models.png
python manage.py graph_models -a -g -o my_project_visualized.png



# function base API
# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.permissions import AllowAny
@api_view(["POST"])
@permission_classes((AllowAny,))
def email_avatar(request):
    if request.method != "POST":
        raise MethodNotAllowed("Just POST Allowed!")
    try:
        email = request.data["email"]
        print(email)
    except KeyError:
        raise ValidationError

# urls.py
urlpatterns = [
	path(r"api/v1/check_email", email_avatar)
]


# Setting Filter in Route using ?eample=""
def get_queryset(self):
    if self.request.query_params.get('author', None) is not None:
        username = self.request.query_params.get('author', None)
        try:
            user_id = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise NotFound
        return Comment.objects.filter(author=user_id)
    else:
        return Comment.objects.all()


# swagger django
# Install Swagger
# pip install django-rest-swagger
# urls.py
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='APP Title')

urlpatterns += [
    path(r'api/v1/swagger/', schema_view)
]



# media URL
# settings.py
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR)
MEDIA_URL = '/uploads/'

# urls.py
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# Django Database Settings PostgreSQL
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USERNAME'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}



# Django REST JWT Authentication, JWT Response Customize
# urls.py
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns += [
    path(r'^api-token-auth/', obtain_jwt_token)
]
# settings.py
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'accounts.serializers.jwt_response_payload_handler'
}

# Customize the Response
# Adding the user dto with JWT
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


# Sqlite3 Problem Django
# export LD_LIBRARY_PATH="/usr/local/lib"export LD_LIBRARY_PATH="/usr/local/lib"


# Get a Variable from Environment
# get_env_variable
import os
from django.core.exceptions import ImproperlyConfigured
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)



# Per Field Permission in Django REST Framework
class PrivateField(serializers.Field):
    def field_to_native(self, obj, field_name):
        """
        Return null value if request has no access to that field
        """
        if obj.created_by == self.context.get('request').user:
            return super(PrivateField, self).field_to_native(obj, field_name)
        return None

# Usage
class UserInfoSerializer(serializers.ModelSerializer):
    private_field1 = PrivateField()
    private_field2 = PrivateField()

    class Meta:
        model = UserInfo

class PrivateField(serializers.ReadOnlyField):

    def get_attribute(self, instance):
        """
        Given the *outgoing* object instance, return the primitive value
        that should be used for this field.
        """
        if instance.created_by == self.context['request'].user:
            return super(PrivateField, self).get_attribute(instance)
        return None
# https://stackoverflow.com/questions/19128793/per-field-permission-in-django-rest-framework