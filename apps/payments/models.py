from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

UserModel = get_user_model()


class PaymentModel(models.Model):
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.DO_NOTHING,
        verbose_name="Пользователь",
    )
    idempotency_key = models.UUIDField(
        verbose_name="Ключ идемпотентности",
    )
    payment_id = models.CharField(
        verbose_name="ID платежа",
        max_length=100,
    )
    amount = models.DecimalField(
        verbose_name="Цена",
        max_digits=settings.PAYMENT_MAX_DIGITS,
        decimal_places=settings.PAYMENT_DECIMAL_PLACES,
    )
    description = models.CharField(
        verbose_name="Описание",
        max_length=255,
    )
    is_paid = models.BooleanField(
        verbose_name="Оплачен",
        default=False,
    )
    is_closed = models.BooleanField(
        verbose_name="Закрыт",
        default=False
    )
    create_date = models.DateTimeField(
        verbose_name="Время создания",
    )
    close_date = models.DateTimeField(
        verbose_name="Время закрытия",
        null=True,
        blank=True
    )
    check_file = models.FileField(
        verbose_name="Файл чека",
        upload_to='checks/',
        null=True,
    )

    @classmethod
    def check_success(cls, user_id: int):
        try:
            payment = PaymentModel.objects.get(
                user_id=user_id,
                is_paid=True
            )
            if payment:
                return True
        except ObjectDoesNotExist:
            pass

        return False

    def __str__(self):
        return f"Payment {self.payment_id}"

    class Meta:
        verbose_name = "платёж"
        verbose_name_plural = "платежи"
