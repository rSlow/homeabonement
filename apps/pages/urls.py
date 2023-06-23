from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("policy/", views.PolicyPageView.as_view(), name="policy"),
    path("feedback/", views.FeedbackFormView.as_view(), name="feedback"),
    path("offer/", views.OfferPageView.as_view(), name="offer"),
]
