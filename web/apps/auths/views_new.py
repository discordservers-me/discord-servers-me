from django.views import generic
from datetime import datetime
from django.utils.timezone import make_aware
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import RedirectView, View
from django.contrib.auth.views import LogoutView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model, login, logout as auth_logout
from requests_oauthlib import OAuth2Session
# from django.conf import settings
# from . import forms
import os
if settings.DEBUG:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
User = get_user_model()


class ModifiedLoginView(generic.TemplateView):
    # form_class = forms.LoginForm
    # template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        user_id = request.session.get('discord_user_id', False)
        # response = super().get(request, *args, **kwargs)

        if request.user.is_authenticated:
            return redirect('home')
        elif user_id:
            try:
                user = User.objects.get(user_id=user_id)
                login(request, user)
                return redirect('user:dashboard')
            except User.DoesNotExist:
                return redirect('auth:discord')
        else:
            return redirect('auth:discord')


class ModifiedLogoutView(LogoutView):

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        discord_user_id = request.session.get('discord_user_id', False)

        auth_logout(request)

        if settings.DISCORD_EASY_LOGIN:
            # saves the access token for easier relog
            if discord_user_id:
                request.session['discord_user_id'] = discord_user_id
        next_page = self.get_next_page()
        if next_page:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)


def oauth_session(request, state=None, token=None):
    """ Constructs the OAuth2 session object. """
    if settings.DISCORD_REDIRECT_URI is not None:
        redirect_uri = request.build_absolute_uri(reverse(settings.DISCORD_REDIRECT_URI))
    else:
        redirect_uri = request.build_absolute_uri(reverse('discord_callback'))

    scope = (['email', 'identify'] if settings.DISCORD_EMAIL_SCOPE else 'identify')
    return OAuth2Session(
        settings.BOT_ID,
        redirect_uri=redirect_uri,
        scope=scope,
        token=token,
        state=state)


class DiscordAuthorizeView(RedirectView):

    def get(self, request, *args, **kwargs):

        if request.user:
            if request.user.is_authenticated:
                return redirect('user:dashboard')

        discord_user_id = request.session.get('discord_user_id', '')
        if discord_user_id:
            try:
                user = User.objects.get(user_id=discord_user_id)
                login(request, user)
                return redirect('user:dashboard')
            except User.DoesNotExist:
                pass

        response = super().get(request, *args, **kwargs)
        return response

    def get_redirect_url(self, *args, **kwargs):

        discord_oauth2_data = self.request.session.get('discord_oauth2_data', False)

        # already authenticated via discord
        if discord_oauth2_data:
            return reverse('auth:discord_callback')

        else:
            API_BASE_URL = 'https://discordapp.com/api'
            AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'

            oauth = oauth_session(self.request)
            authorization_url, state = oauth.authorization_url(AUTHORIZATION_BASE_URL)
            self.request.session['discord_oauth2_state'] = state
            return authorization_url


class DiscordCallbackView(View):

    def get(self, request, *args, **kwargs):

        API_BASE_URL = 'https://discordapp.com/api'
        TOKEN_URL = API_BASE_URL + '/oauth2/token'
        USER_INFO_URL = API_BASE_URL + '/users/@me'

        state = request.GET.get('state', None)
        if state is not None and state == request.session.get('discord_oauth2_state', ''):
            code = request.GET.get('code')
            oauth = oauth_session(request, state=state)

            # get token info
            token = oauth.fetch_token(
                TOKEN_URL,
                authorization_response=request.build_absolute_uri(),
                client_secret=settings.BOT_SECRET,
                code=code)

            # get user info
            user = oauth.get(USER_INFO_URL).json()

            # store information from user and token to a single place
            data = self.decompose_data(user, token)

            # state cleanup
            del request.session['discord_oauth2_state']

            # log the user in or create new user
            try:
                user = User.objects.get(user_id=data['user_id'])
            except User.DoesNotExist:
                user = User.objects.create_user(
                    user_id=data['user_id'], password=data['access_token'],
                )

            # add additional account information into the User instance
            user.username = data.get('username', '')
            user.discriminator = data.get('discriminator', '')
            user.discord_email = data.get('discord_email', '')
            user.avatar = data.get('avatar', '')
            user.access_token = data.get('access_token', '')
            user.refresh_token = data.get('refresh_token', '')
            user.scope = data.get('scope', '')
            try:
                expiry = datetime.utcfromtimestamp(float(data['expiry']))
                if settings.USE_TZ:
                    expiry = make_aware(expiry)
                user.expiry = expiry
            except (ValueError, KeyError):
                pass

            user.save()

            # save discord user_id for easy authentication
            request.session['discord_user_id'] = data.get('user_id', '')

            if user is not None:
                login(request, user)
                return redirect('user:dashboard')
            else:
                return HttpResponseForbidden('User not found.')
        else:
            error = request.GET.get('error', None)
            if error == 'access_denied':
                return redirect('auth:login')
            return HttpResponseForbidden('Invalid request.')

    def decompose_data(self, user, token):
        """ Extract the important details from user and token """
        data = {
            'user_id': user['id'],
            'username': user['username'],
            'discriminator': user['discriminator'],
            'discord_email': user.get('email', ''),
            'avatar': user.get('avatar', ''),
            'access_token': token['access_token'],
            'refresh_token': token.get('refresh_token', ''),
            'scope': ' '.join(token.get('scope', '')),
            'expiry': token.get('expires_at', ''),
        }
        for k in data:
            if data[k] is None:
                data[k] = ''
        return data
