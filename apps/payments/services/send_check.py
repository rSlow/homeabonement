from django.conf import settings
from django.core.mail import EmailMessage

from apps.pages.services.email_renderer import PremailerRenderer
from apps.payments.models import PaymentModel


def get_subject(payment_object: PaymentModel):
    return " ".join([
        f"Кассовый чек № {payment_object.pk} от",
        f"{payment_object.create_date:{settings.TIME_FORMAT}} -",
        f"Онлайн-курс ДОМАШНИЙ АБОНЕМЕНТ"
    ])


def get_body(payment_object: PaymentModel, context: dict):
    payment_context = {
        "payment_id": payment_object.payment_id,
        "payment_amount": payment_object.amount,
    }
    context.update(payment_context)
    body = PremailerRenderer.render(
        template_name="payments/email/check.html",
        context=context
    )
    return body


def send_check(payment_object: PaymentModel, context: dict):
    check_file = payment_object.check_file
    message = EmailMessage(
        subject=get_subject(payment_object=payment_object),
        body=get_body(payment_object=payment_object, context=context),
        to=[payment_object.user.email]
    )
    message.content_subtype = 'html'
    message.attach(
        filename=check_file.name,
        content=check_file.file.read(),
        mimetype=check_file.file.content_type
    )
    message.send()
