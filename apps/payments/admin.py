from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import format_html

from .models import PaymentModel


@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'user', 'amount', 'description', 'is_paid', 'create_date', 'close_date',
                    'is_check_sent', 'check_file', 'send_check']
    list_filter = ["is_paid", "is_check_sent"]
    search_fields = ["user__email"]
    change_form_template = 'admin/payments/change.html'

    def render_change_form(self, request, context, add=False, change=False, form_url="", obj=None):
        if context is None:
            context = {}
        if obj and change:
            context["send_cheque_url"] = reverse_lazy("send_check", kwargs={'payment_id': obj.payment_id})
        return super().render_change_form(request, context, add, change, form_url, obj)

    def send_check(self, obj: PaymentModel):
        if obj.is_paid:
            if not obj.is_check_sent:
                url = reverse_lazy("send_check", kwargs={'payment_id': obj.payment_id})
                return format_html('<a href="{}">Отправить чек</a>', url)
            else:
                return "Чек отправлен"
        else:
            return ""

    send_check.short_description = "Отправка чека"
