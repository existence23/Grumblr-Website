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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from grumblr import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('grumblr/register', views.register),
    path('', views.home),
    path('grumblr', views.home),
    path('grumblr/login', views.self_login),
    path('grumblr/logout', views.self_logout),
    path('grumblr/add-post', views.add_post),
    path('grumblr/check-profile/<int:user_id>', views.check_profile),
    path('grumblr/delete-post/<int:post_id>', views.delete_post),
    path('grumblr/delete-user', views.delete_account),
    path('grumblr/complete-file', views.complete),
    path('grumblr/personal-info', views.check_personal),
    path('grumblr/modify-firstname', views.modify_firstname),
    path('grumblr/modify-lastname', views.modify_lastname),
    path('grumblr/modify-username', views.modify_username),
    path('grumblr/modify-password', views.modify_password),
    path('grumblr/modify-bio', views.modify_bio),
    path('grumblr/modify-age', views.modify_age),
    path('grumblr/modify-photo', views.modify_photo),
    path('grumblr/follow/<int:post_id>', views.follow),
    path('grumblr/unfollow/<int:post_id>', views.unfollow),
    path('grumblr/follower-stream', views.check_follower),
    path('grumblr/confirm-email', views.confirm_email),
    url(r'^email/(?P<active_code>.*)/$', views.verify),
    url(r'^change-password/(?P<active_code>.*)/$', views.confirm_change_password),
    path('change-password/<active_code>/modify-password', views.modify_password),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
