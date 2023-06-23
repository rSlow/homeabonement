from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path("create/", views.CreatePaymentView.as_view(), name="create_payment"),
    path("send-check/<int:pk>/", views.SendCheckFormView.as_view(), name="send_check"),

    # for yoomoney hook
    path("acceptance/", csrf_exempt(views.AcceptancePaymentView.as_view()), name="acceptance_payment"),
]
