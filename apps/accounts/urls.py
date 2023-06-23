from django.urls import path

from .views import CustomPasswordResetView

urlpatterns = [
    path(
        "password/reset/",
        CustomPasswordResetView.as_view(),
        name="account_reset_password"
    ),
]
