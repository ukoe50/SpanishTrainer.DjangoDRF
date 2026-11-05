-------------------------------------------------------------------------------------------------
Setup Django project (with PyCharm)
-------------------------------------------------------------------------------------------------
# Create new project with virtual environment (venv)
> python --version
# pip freeze ist ein Befehl in Python, der die aktuell installierten Pakete und ihre Versionen in
# einer virtuellen Umgebung auflistet
> pip --version
> pip install django
> django-admin --version
> django-admin startproject voctrainer
> python manage.py runserver
# open http://127.0.0.1:8000/
# An app is a web application that has a specific meaning in your project, like a home page, a contact
# form, or a members database
> python manage.py startapp words



-------------------------------------------------------------------------------------------------
MySQL Client Connect
-------------------------------------------------------------------------------------------------
> pip install mysqlclient

Successfully installed mysqlclient-2.2.7

settings.py:
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'spanishtrainer.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spanishtrainer',
        'USER': 'root',
        'PASSWORD': 'Paxxword123!',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}



-------------------------------------------------------------------------------------------------
Django logging
-------------------------------------------------------------------------------------------------
# https://dev.to/kuba_szw/django-logging-forget-about-print-when-debugging-3g11
# Go to your settings.py and prepare the LOGGING dict. This is the basic configuration
# that you will probably see in your console

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }
}

import logging
logger = logging.getLogger('django')

logger.info('here goes your message')



-------------------------------------------------------------------------------------------------
Setup Django Rest Framework (DRF) project (with PyCharm)
-------------------------------------------------------------------------------------------------
https://www.django-rest-framework.org/
> pip install django
> pip install djangorestframework
> django-admin startproject myapi .
# rename, set database settings settings.py
> python manage.py runserver
> http://127.0.0.1:8000
> http://127.0.0.1:8000/admin
# add models.py file and content
# add framework and apps to INSTALLED_APPS in settings.py
	'rest_framework',  
    'api',  
> python manage.py migrate
> python manage.py makemigrations myapi
> python manage.py migrate
# add model classes to admin.py to define automatic CRUD
# create superuser
> python manage.py createsuperuser
# customize ModelClasses in admin.py
# define serializers.py
	Raw Serializers
	Flat Serializers
	Nested Serializers
	Custom Serializers
# define urls/routes
# define views.py
# Function Based Views Cons
	Hard to extend and reuse the code
	Handling of HTTP methods via conditional branching
	!!! The browsable API only works with Response not with JsonResponse 
	for Function Based Views
# Class Based Views
	DRY — Using CBVs help to reduce code duplication
# Generic Views	(based on Class based views)
	ListAPIView
	RetrieveAPIView
	
# QuerySet methods
# https://docs.djangoproject.com/en/5.2/topics/db/queries/
	Filter (AND, OR)
	Order
	Limit



-------------------------------------------------------------------------------------------------
Common REST Conventions	
-------------------------------------------------------------------------------------------------
https://metamug.com/article/rest-api-naming-best-practices.html#1-using-commonly-used-nouns-as-resource-names
#
# For example:
#
# GET    /resources - returns a list of resource items
# POST   /resources - creates one or many resource items
# PUT    /resources - updates one or many resource items
# PATCH  /resources - partially updates one or many resource items
# DELETE /resources - deletes all resource items
#
# And for single resource items:
#
# GET    /resources/:id - returns a specific resource item based on :id parameter
# POST   /resources/:id - creates one resource item with specified id (requires validation)
# PUT    /resources/:id - updates a specific resource item
# PATCH  /resources/:id - partially updates a specific resource item
# DELETE /resources/:id - deletes a specific resource item
#
# Related data:
#
# GET  /orders/1/lines  <---> orders[1].lines
# POST /orders/1/lines  <---> orders[1].lines.push(data)	


-------------------------------------------------------------------------------------------------
Django User Auth & Autorization
-------------------------------------------------------------------------------------------------
If you’re starting a new project, it’s highly recommended to set up a custom user model

settings.py:
AUTH_USER_MODEL = 'myapp.MyUser'

example: AUTH_USER_MODEL="spanishtrainer_api.User"

models.py:
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
	
	
Now the reference to a user can be used by using a foreign key in some other table:	
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=null)
	
!!! ValueError: The field admin.LogEntry.user was declared with a lazy reference to 'spanishtrainer_api.user', but app 
	'spanishtrainer_api' doesn't provide model 'user'.
	We have to remove all migrations from our project by
Solved:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	Then delete the database.Then run migrations & migrate again.
	python manage.py makemigrations 
	python manage.py migrate
	

Use Django Admin for Account Management:
At the top, import include and create a new URL path at accounts/. You can choose a different URL path, but using 
accounts/ is a standard practice and requires less customization later

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # new
]

INSTALLED_APPS = [
	...
    'django.contrib.auth',
    ...
]

Also, register the model in the app’s admin.py:

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)



-------------------------------------------------------------------------------------------------
Setting up JWT Auth for Django Rest Framework wiht simplejwt
-------------------------------------------------------------------------------------------------
https://www.django-rest-framework.org/api-guide/authentication/

# override
def get_permissions(self):
	if self.request.method == 'GET':
		self.permission_classes = [AllowAny]
	else:
		# IsAuthenticated, IsAdminUser, etc
		# if not Authenticated: HTTP 403 Forbidden
		self.permission_classes = [IsAuthenticated]
	return super().get_permissions()

> pip install djangorestframework-simplejwt

INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
    ...
]

REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )

Add to urls.py:
path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	
TokenObtainPairView contains 2 Tokens!

!!! Error  "detail": "No active account found with the given credentials"
	Reason: No hashed password!
	
override create for a Custom User: class User(AbstractUser)
		
		
		
-------------------------------------------------------------------------------------------------
drf-spectacular Open API 3, Swagger 
-------------------------------------------------------------------------------------------------
https://medium.com/@anindya.lokeswara/efficient-api-development-in-django-rest-framework-drf-spectacular-and-postman-workspace-4dd6f860d14d

> pip install drf-spectacular

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
}

INSTALLED_APPS = [
	...
    'drf_spectacular'
]

urlpatterns = [
    ...
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ...
]


-------------------------------------------------------------------------------------------------
Django REST Framework Ordering and Filtering (with Query Params)
-------------------------------------------------------------------------------------------------
> pip install django-filter

INSTALLED_APPS = [
	...
    'django_filters'
]

REST_FRAMEWORK = {
	...
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

class WordFilter(django_filters.FilterSet):
    class Meta:
        model = Word
		fields = {
            'level': ['exact', 'lt', 'gt', 'range'],
            'wordtype' : ['exact'],
            'es' : ['exact', 'contains']
        }

# define in View class:
# define filter directly without FilterSet
#filterset_fields = ['level', 'wordtype']
filterset_class = WordFilter	

# default for 'exact': case sensitive --> ?es=¡Buenas tArdes! is not found!
# default for 'contains': ignore case
# example: ?level__gt=2
# example: ?level__lt=2
# example 'exact': ?es=¡Hola!
# example 'contains': ?es__contains=Hola
# example 'contains': # ?es__contains=¡Buenas tardes!
# example 'contains': # ?es__contains=¡buenas tardes!
# example 'contains': # ?es__contains=tardes
# !!! but: no word match: ?es__contains=el	


Ordering and Search:
# define in View class:
filter_backends = [
	DjangoFilterBackend,
	filters.SearchFilter,
	filters.OrderingFilter,
]
#search_fields = ['=es', '=de']
search_fields = ['es', 'de']
ordering_fields = ['id', 'es', 'de', 'level', 'wordtype', 'seqnumber']
# example: ?search=Buen
# example: ?search=Hola
# example: ?search=Hallo
# example: ?ordering=de