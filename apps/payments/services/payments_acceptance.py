from datetime import datetime, timedelta
import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.urls import reverse
from yookassa import Payment
from django.conf import settings
from yookassa.domain.exceptions import BadRequestError
from yookassa.domain.notification import WebhookNotification

from apps.payments.models import PaymentModel
from apps.payments.schemas import PaymentStatuses

UserModel = get_user_model()


class NoConfirmationError(BadRequestError):
    pass


def create_payment(user_id: int,
                   amount: int,
                   description: str,
                   force: bool = False):
    try:
        if force:
            raise ObjectDoesNotExist
        else:
            db_payment = PaymentModel.objects.get(user_id=user_id)
            now = datetime.now().astimezone()

            if now - db_payment.create_date > timedelta(hours=24):
                db_payment.delete()
                raise ObjectDoesNotExist
            else:
                idempotency_key = db_payment.idempotency_key

    except ObjectDoesNotExist:
        idempotency_key = uuid.uuid4()
        db_payment = PaymentModel(
            user_id=user_id,
            amount=amount,
        )

    try:
        payment = get_payment_object(
            amount=amount,
            description=description,
            user_id=user_id,
            idempotency_key=idempotency_key
        )
        if payment.confirmation is None:
            raise NoConfirmationError
    except (BadRequestError, NoConfirmationError):
        return create_payment(
            user_id=user_id,
            amount=amount,
            description=description,
            force=True
        )

    db_payment.payment_id = payment.id
    db_payment.idempotency_key = idempotency_key
    db_payment.create_date = datetime.fromisoformat(payment.created_at)
    db_payment.save()

    return payment


def get_payment_object(amount: int,
                       description: str,
                       user_id: int,
                       idempotency_key: uuid.UUID):
    payment = Payment.create(
        params={
            "amount": {
                "value": amount,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": settings.DOMAIN + reverse('profile')
            },
            "capture": True,
            "description": description,
            "metadata": {
                "user_id": user_id,
                "idempotency_key": idempotency_key.hex
            },
            "refundable": False,
        },
        idempotency_key=idempotency_key
    )
    return payment


def get_payment_acceptance_response(payment: WebhookNotification):
    event = payment.event

    match event:
        case PaymentStatuses.succeeded.value:
            payment_object = payment.object
            payment_id = payment_object.id

            try:
                payment = PaymentModel.objects.get(payment_id=payment_id)
                payment.is_paid = True
                payment.is_closed = True
                payment.close_date = payment_object.captured_at
                payment.save()

                user = UserModel.objects.get(id=payment.user_id)
                user.is_course_purchased = True
                user.save()

            except ObjectDoesNotExist:
                try:
                    payment = PaymentModel(
                        user_id=payment_object.metadata["user_id"],
                        payment_id=payment_object.id,
                        amount=payment_object.amount.value,
                        idempotency_key=uuid.uuid4(),
                        is_paid=True,
                        is_closed=True,
                        create_date=payment_object.created_at,
                        close_date=payment_object.captured_at
                    )
                    payment.save()
                except Exception as ex:
                    return HttpResponse(status=500)

            return HttpResponse(status=200)

        case PaymentStatuses.canceled.value:
            return HttpResponse(status=200)
