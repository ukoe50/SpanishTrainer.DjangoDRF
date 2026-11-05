"""
URL configuration for spanishtrainer_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns: path('', views.home, name='home')
Class-based views
    1. Add an import: from other_app.views import Home
    2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from spanishtrainer_api import views
from spanishtrainer_api.views import WordList, WordDetail, WordListAPIView, WordDetailAPIView, WordTypeListAPIView, \
    CategoryListAPIView, WordCreateAPIView, WordListCreateAPIView, WordDetailRetrieveUpdateDestroyAPIView, \
    CategoryWordListAPIView, CategoryDetailRetrieveAPIView, AddWordToCategoryCreateAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
# from spanishtrainer_api.views.classbased import WordList, WordDetail
# from spanishtrainer_api import views

# all urls for app, includes function- and classbased views
# change the default <int:pk> to <int:id> for generic views and
urlpatterns = [
    path('admin/', admin.site.urls),
    # path("accounts/", include("django.contrib.auth.urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/register/', views.ContentUserRegisterView.as_view(), name='auth_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/words/', WordListCreateAPIView.as_view()),
    path('api/words/<int:id>', WordDetailRetrieveUpdateDestroyAPIView.as_view()),
    path('api/wordtypes/', WordTypeListAPIView.as_view()),
    path('api/categorys/', CategoryListAPIView.as_view()),
    path('api/categorys/<int:categoryid>', CategoryDetailRetrieveAPIView.as_view()),
    path('api/categorys/<int:categoryid>/words', CategoryWordListAPIView.as_view()),
    # path('api/categorys/<int:categoryid>/words/<int:wordid>', AddWordToCategoryCreateAPIView.as_view()),
    path('api/categorys/<int:categoryid>/words/<int:wordid>', views.addWordToCategory),
]

# for testing purpose:
# path('api/functionbased/words/', views.word_list),
# path('api/functionbased/words/<int:id>', views.word_details),
# path('api/functionbased/wordtypes/', views.wordtype_list),
# path('api/functionbased/wordtypes/<int:id>', views.wordtype_details),
# path('api/classbased/words/', WordList.as_view()),
# path('api/classbased/words/<int:id>', WordDetail.as_view()),
# path('api/generic/words/getlist', WordListAPIView.as_view()),
# path('api/generic/words/create', WordCreateAPIView.as_view()),


#
# an alternative is including urls.py files
#
# urlpatterns = [
#     path('api/', include('projects.urls')),
# ]

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