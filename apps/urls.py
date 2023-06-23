from django.urls import path, include

urlpatterns = [
    path("accounts/", include("apps.accounts.urls")),
    path("course/", include("apps.courses.urls")),
    path("payments/", include("apps.payments.urls")),
    path("", include("apps.pages.urls")),
]
