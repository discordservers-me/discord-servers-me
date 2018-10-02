from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from web.apps.core.views import HomeView
from . import settings

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('admin/', admin.site.urls),
    path('u/', include('web.apps.users.urls')),
    path('auth/', include('web.apps.auths.urls')),
    path('giveaway/', include('web.apps.giveaways.urls')),
    path('servers/', include('web.apps.servers.urls')),
    path('partners/', include('web.apps.partners.urls')),
    path('premium/', include('web.apps.premiums.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('summernote/', include('django_summernote.urls')),
    path(settings.DISCORD_TAIL_URL, RedirectView.as_view(url=settings.DISCORD_INVITE_LINK), name='discord_server')

]

