from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import LoginForm, ResetPasswordForm
from .models import CustomUser

captcha_placeholder = "Введите символы на картинке (на английском языке)"


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = ["login", "password"]
        for field in fields:
            del self.fields[field].widget.attrs['placeholder']


class CustomResetPasswordForm(ResetPasswordForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields["captcha"].widget.attrs['placeholder'] = captcha_placeholder


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['email', 'username']


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        block_fields = ["email", "username"]
        for field in block_fields:
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone', 'first_name', 'last_name',
                  'sex', 'photo',)
