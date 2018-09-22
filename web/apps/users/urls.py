from django.urls import path

from .views import UserDashboardView

app_name = 'user'

urlpatterns = [
    path('dashboard', UserDashboardView.as_view(), name='dashboard'),
]
