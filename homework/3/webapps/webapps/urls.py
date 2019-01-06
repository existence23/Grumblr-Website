"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from grumblr import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('grumblr/register', views.register),
    path('', views.register),
    path('grumblr', views.home),
    path('grumblr/login', views.self_login),
    path('grumblr/logout', views.self_logout),
    path('grumblr/add-post', views.add_post),
    path('grumblr/check-profile/<int:user_id>', views.check_profile),
    path('grumblr/delete-post/<int:post_id>', views.delete_post),
    path('grumblr/delete-user', views.delete_account),
]
