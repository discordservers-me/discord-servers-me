from django.urls import path

from . import views

app_name = 'giveaway'

urlpatterns = [
    path('', views.GiveAwayView.as_view(), name='detail'),
]
