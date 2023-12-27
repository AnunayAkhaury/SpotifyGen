
from django.urls import path
from .views import AuthenticationURLView, spotify_redirect, CheckAuthentication, CreatePlaylist

urlpatterns = [
    path("auth-url", AuthenticationURLView.as_view()),
    path("redirect", spotify_redirect),
    path("check_auth", CheckAuthentication.as_view()),
    path("CreatePlaylist", CreatePlaylist.as_view()),  
]
