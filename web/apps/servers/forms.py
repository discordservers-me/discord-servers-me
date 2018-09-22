from django import forms
from material import *

from .models import DiscordServer


class UpdateServerForm(forms.ModelForm):

    layout = Layout(
        'premium_highlight',
        'short_description',
        'description',
        'invite_link',
        'shown',
        'tags',
        'website',

    )

    class Meta:
        model = DiscordServer
        fields = (
            'short_description',
            'description',
            'invite_link',
            'shown',
            'website',
            'tags',
            'premium_highlight'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['short_description'].help_text = 'Show what your server is about. This short description will be shown in the server\'s card.'  # noqa e501
        self.fields['description'].help_text = 'Describe in details about your server. Catch the searchers\' interests when they click on your server card!'  # noqa e501
        self.fields['tags'].help_text = 'Add tags for more server exposure when a user searches for a relevant tag.'  # noqa e501
        self.fields['invite_link'].label = 'Discord Invite Link (PERMANENT)'
        self.fields['shown'].help_text = 'Check this to make the server visible.'  # noqa e501
        self.fields['website'].help_text = 'We\'d love to visit your server\'s website! And of course users who search this server out would, too!'  # noqa e501

    def clean_invite_link(self):
        invite_link = self.cleaned_data.get('invite_link')

        if not invite_link:
            self.add_error('invite_link', 'An invite link must be provided for the server to be publicly visible.')
            return
        elif not invite_link.startswith('https://discord.gg/'):
            self.add_error('invite_link', 'Please provide a valid Discord invite link.')
            return
        return invite_link

    def clean_premium_highlight(self):

        premium_highlight = self.cleaned_data.get('premium_highlight', None)
        server_tier = self.instance.premium_tier
        if premium_highlight in [1, 2]:
            if server_tier == 0:
                self.add_error('premium_highlight', 'The server must have at least Premium Tier 1 to choose a highlight color.')
            else:
                return premium_highlight
        elif premium_highlight == 3:
            if server_tier != 2:
                self.add_error('premium_highlight', 'The server must have Premium Tier 2 to choose this highlight color.')
            else:
                return premium_highlight
        else:
            return premium_highlight
