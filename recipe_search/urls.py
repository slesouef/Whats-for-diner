"""recipe_search URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from accounts import views as accounts_views
from recipes import views as recipes_views
from search import views as search_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/signup', accounts_views.signup, name='signup'),
    path('account/profile', accounts_views.profile, name='profile'),
    path('account/update', accounts_views.update, name='update'),
    path('account/delete', accounts_views.delete, name='delete'),
    path('account/login', accounts_views.user_login, name='login'),
    path('logout', accounts_views.user_logout, name='logout'),
    path('recipe/create', recipes_views.create_recipe, name='recipeCreate'),
    path('recipe/details/<int:rid>',
         recipes_views.recipe_details, name='details'),
    path('recipe/update/<int:rid>',
         recipes_views.update_recipe, name='recipeUpdate'),
    path('recipe/list', recipes_views.show_list, name='userList'),
    path('recipe/vote/<int:rid>', recipes_views.add_vote_result, name='vote'),
    path('', search_views.landing, name='landing'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
