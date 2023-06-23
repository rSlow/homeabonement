from django import forms
from django.conf import settings

from .models import PaymentModel


class CreatePaymentForm(forms.Form):
    description = forms.CharField(
        max_length=255,
        label="Описание",
    )
    amount = forms.DecimalField(
        decimal_places=settings.PAYMENT_DECIMAL_PLACES,
        max_digits=settings.PAYMENT_MAX_DIGITS,
        label="Сумма",
    )
    user_id = forms.IntegerField(
        label="Пользователь"
    )


class SendPaymentCheckForm(forms.ModelForm):
    email = forms.EmailField(
        label="Электронная почта",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        self.fields['email'].initial = instance.user.email

        block_fields = ["email", "payment_id"]
        for field in block_fields:
            self.fields[field].widget.attrs['readonly'] = True
    
    class Meta:
        model = PaymentModel
        fields = ['email', 'payment_id', "check_file"]
