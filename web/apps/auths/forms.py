from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import validate_email
from material import *
User = get_user_model()


class LoginForm(AuthenticationForm):

    layout = Layout(
        'username',
        'password'
    )


class CustomSignUpForm(UserCreationForm):

    layout = Layout(
        'email',
        'password1',
        'password2'
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # print(dir(self.fields['password1']))
        # print(self.fields['password1'].widget.attrs)
        self.fields['email'].validators = [validate_email]
        self.fields['password1'].help_text = 'Password must contain at least 8 characters.'
        self.fields['password2'].label = 'Re-enter Password'
        self.fields['password2'].help_text = ''
        if self.initial:
            self.fields['email'].widget.attrs.update({'autofocus': False})
            self.fields['password1'].widget.attrs.update({'autofocus': True})
