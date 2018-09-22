from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):

    email = models.CharField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    user_id = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=32, blank=True)
    discriminator = models.CharField(max_length=4, blank=True)
    avatar = models.CharField(max_length=50, blank=True)
    discord_email = models.CharField(max_length=100, blank=True, null=True, unique=True)

    access_token = models.CharField(max_length=50, blank=True)
    refresh_token = models.CharField(max_length=50, blank=True)
    scope = models.CharField(max_length=200, blank=True)
    expiry = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_name_tag(self):
        """Returns the Discord Username tag (CoolBoy#1337)"""
        return f'{self.username}#{self.discriminator}'

    def avatar_url(self):
        if self.avatar:
            if self.avatar.startswith('a_'):
                url = f'https://cdn.discordapp.com/avatars/{self.user_id}/{self.avatar}.gif'
            else:
                url = f'https://cdn.discordapp.com/avatars/{self.user_id}/{self.avatar}.png'
            return url
        else:
            return f'{settings.STATIC_URL}img/discord_icon.png'
