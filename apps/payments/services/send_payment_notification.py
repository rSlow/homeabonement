from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse

from apps.payments.models import PaymentModel


def get_message_subject(payment_object: PaymentModel):
    return f"Уведомление прошедшем о платеже от {payment_object.user.email}"


def get_message_body(payment_object: PaymentModel):
    domain = settings.ENV.str("DOMAIN")
    admin_payment_link = domain + reverse("admin:payments_paymentmodel_change", args=[payment_object.id])
    send_cheque_link = domain + reverse("send_check", kwargs={'payment_id': payment_object.payment_id})
    context = {
        "payment_id": payment_object.payment_id,
        "admin_payment_link": admin_payment_link,
        "send_cheque_link": send_cheque_link
    }
    return render_to_string(
        template_name="payments/email/send_payment_notification.html",
        context=context
    )


def send_payment_notification_message(payment_object: PaymentModel):
    message = EmailMessage(
        subject=get_message_subject(payment_object=payment_object),
        body=get_message_body(payment_object=payment_object),
        to=[settings.ENV.str("EMAIL_ADMIN")]
    )
    message.send()
