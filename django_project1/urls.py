"""django_project1 URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("blog.urls")),
    path("messaging/",include("messaging.urls")),
    path("register/",user_views.register, name = "register"),
    path("login/",auth_views.LoginView.as_view(template_name = "users/login.html"), name = "login"),
    path("logout/",auth_views.LogoutView.as_view(template_name = "users/logout.html"), name = "logout"),
    path("profile/",user_views.profile, name = "profile"),
    path("publicprofileslist/",user_views.PublicProfilesListView.as_view(template_name = "users/public_profile_list.html"),name = "publicprofileslist"),
    path("publicprofileslist/sortbyfollowers",user_views.FollowersPublicProfilesListView.as_view(template_name = "users/public_profile_list.html"),name = "publicprofileslist-sortbyfollowers"),
    path("publicprofiles/<int:pk>/",user_views.PublicProfileDetailView.as_view(template_name = "users/public_profile_detail.html"),name = "publicprofiles"),
    path('publicprofileslist/search/', user_views.PublicProfilesSearchResultsPostListView.as_view(template_name = "users/public_profile_list.html"), name="user-search"),
    path('publicprofiles/<int:pk>/follow/', user_views.UserFollow, name="user-follow"),
    path('userfollowing/<int:pk>/',user_views.UserFollowingView.as_view(template_name = "users/following.html"), name = "user-following"),
    path('userfollowedby/<int:pk>/',user_views.UserFollowedByView.as_view(template_name = "users/followed_by.html"), name = "user-followed-by"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
