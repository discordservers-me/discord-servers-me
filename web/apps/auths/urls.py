from django.urls import path
# from django.contrib.auth.views import LogoutView
from . import views_new as views

app_name = 'auth'

urlpatterns = [
    path('discord', views.DiscordAuthorizeView.as_view(), name='discord'),
    path('discord/callback', views.DiscordCallbackView.as_view(), name='discord_callback'),
    path('login', views.ModifiedLoginView.as_view(), name='login'),
    path('logout', views.ModifiedLogoutView.as_view(), name='logout'),
    # path('signup', views.SignUpView.as_view(), name='signup'),
]
