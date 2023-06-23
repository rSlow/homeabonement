from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

User = get_user_model()


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    yes_icon = '<img src="/static/admin/img/icon-yes.svg" alt="True">'
    no_icon = '<img src="/static/admin/img/icon-no.svg" alt="False">'

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['email', 'username', 'first_name', 'last_name', "is_course_purchased", "is_email_confirmed"]
    list_filter = ["is_course_purchased"]
    search_fields = ["email", "username"]
    actions = ["make_verified", "make_course_purchased"]
    readonly_fields = ["is_email_confirmed"]

    fieldsets = (
        (None, {"fields": ("username",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "sex", "phone", "is_email_confirmed")}),
        ("Курсы", {"fields": ("is_course_purchased",)}),
        (_("Permissions"), {"fields": (
            "is_active",
            "is_staff",
            "is_superuser",
        )}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request=request).prefetch_related("emailaddress_set")
        return qs

    def is_email_confirmed(self, obj: CustomUser):
        if obj.emailaddress_set.first().verified:
            return format_html(self.yes_icon)
        else:
            return format_html(self.no_icon)

    def make_verified(self, _, queryset):
        users: list[CustomUser] = queryset.all()
        id_list = [user.id for user in users]
        EmailAddress.objects.filter(user_id__in=id_list).update(verified=True)

    def make_course_purchased(self, _, queryset):
        queryset.update(is_course_purchased=True)

    is_email_confirmed.short_description = "Подтверждён"
    make_verified.short_description = "Отметить выбранные e-mail адреса как подтвержденные"
    make_course_purchased.short_description = "Отметить оплату курса"


admin.site.unregister(Group)
admin.site.unregister(EmailAddress)
admin.site.unregister(Site)
