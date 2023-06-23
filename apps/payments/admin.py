from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import format_html

from .models import PaymentModel


@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PaymentModel._meta.get_fields()] + ['send_check']
    list_filter = ["is_paid"]
    search_fields = ["user__email"]

    def send_check(self, obj: PaymentModel):
        if not obj.check_file:
            url = reverse_lazy("send_check", kwargs={'pk': obj.id})
            return format_html('<a href="{}">Отправить чек</a>', url)
        else:
            return "Чек отправлен"
    send_check.short_description = "Отправка чека"
