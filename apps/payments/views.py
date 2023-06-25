import json

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView
from yookassa.domain.notification import WebhookNotification

from config.context_processors import env_ctx_processor
from config.permissions import CourseNotPurchaseRequired, AdminRequired
from config.settings import ENV
from .exceptions import CheckAlreadySentException
from .forms import CreatePaymentForm, SendPaymentCheckForm
from .models import PaymentModel
from .services.client_ip import get_client_ip, is_ip_valid
from .services.payments_acceptance import get_payment_acceptance_response, create_payment
from .services.send_check import send_check


class CreatePaymentView(CourseNotPurchaseRequired, FormView):
    form_class = CreatePaymentForm
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        if not ENV.bool("PAYMENT_POSSIBLE", default=False):
            return redirect('home')

        data = self.get_form().data

        payment = PaymentModel.objects.get_paid_or_none(user_id=data["user_id"])
        if payment:
            payment_id = payment.payment_id
            return render(
                request=request,
                status=400,
                template_name='payments/already_purchased_payment.html',
                context={"payment_id": payment_id}
            )
        else:
            payment = create_payment(
                user_id=data["user_id"],
                amount=data["amount"],
                description=data["description"],
            )
            return HttpResponseRedirect(
                redirect_to=payment.confirmation.confirmation_url,
            )


class AcceptancePaymentView(UpdateView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        client_ip = get_client_ip(request=request)
        if not is_ip_valid(client_ip):
            return HttpResponse(status=403)

        notification_json = json.loads(request.body)
        notification_object = WebhookNotification(notification_json)
        response = get_payment_acceptance_response(notification_object)

        return response


class SendCheckFormView(AdminRequired, UpdateView):
    template_name = 'payments/send_check_form.html'
    form_class = SendPaymentCheckForm
    model = PaymentModel

    def get_object(self, queryset=None):
        obj: PaymentModel = super().get_object(queryset=queryset)
        if obj.is_check_sent:
            messages.add_message(
                request=self.request,
                level=messages.WARNING,
                message="Чек уже был отправлен."
            )
            raise CheckAlreadySentException
        return obj

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except CheckAlreadySentException:
            return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ctx = env_ctx_processor(self.request)
        context.update(ctx)
        return context

    def form_valid(self, form):
        payment: PaymentModel = self.object
        context = self.get_context_data()

        try:
            send_check(
                payment_object=payment,
                context=context
            )
            messages.add_message(
                request=self.request,
                level=messages.SUCCESS,
                message="Чек успешно отправлен."
            )

            payment.is_check_sent = True
            payment.save()

            return super().form_valid(form=form)

        except Exception as ex:
            messages.add_message(
                request=self.request,
                level=messages.ERROR,
                message=f"Ошибка при отправке чека - {ex}"
            )
            return super().form_invalid(form=form)

    def get_success_url(self):
        return reverse_lazy("admin:payments_paymentmodel_changelist")
