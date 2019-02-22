from django import forms
from web.apps.servers.models import DiscordServer


class UserServersForm(forms.Form):
    server = forms.ChoiceField(
        label=''
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        server_choices = DiscordServer.objects.filter(managers__manager_id=self.user.user_id).values_list('pk', 'name')
        self.fields['server'].choices = server_choices
