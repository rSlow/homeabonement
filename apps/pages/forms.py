from captcha.fields import CaptchaField
from django import forms

from .models import FeedbackModel


class FeedbackForm(forms.ModelForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["captcha"].widget.attrs['placeholder'] = "Введите символы на картинке (на английском языке)"

    class Meta:
        model = FeedbackModel
        fields = ["name", "email", "text"]
