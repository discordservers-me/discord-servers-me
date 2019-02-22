from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from material import *
User = get_user_model()


class CustomPasswordChangeForm(PasswordChangeForm):
    layout = Layout(
        'old_password',
        'new_password1',
        'new_password2'
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].help_text = ''
