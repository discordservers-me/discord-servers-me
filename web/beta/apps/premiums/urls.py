from django.urls import path

from . import views

app_name = 'premium'

urlpatterns = [
    path('', views.PremiumView.as_view(), name='detail'),
    path('payment', views.PremiumPaymentView.as_view(), name='payment'),
    path('payment/success', views.PaypalReturnView.as_view(), name='success'),
    path('payment/canceled', views.PaypalCanceledReturnView.as_view(), name='canceled'),
]
