from django.urls import path
from .views import UserDashboardView
app_name = 'user'

urlpatterns = [
    path('dashboard', UserDashboardView.as_view(), name='dashboard'),
    # path('change-password/', CustomPasswordChangeView.as_view(), name='password_change'),
]
