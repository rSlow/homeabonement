from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name='profile'),
    path("delete-photo/", views.RemoveProfilePhoto.as_view(), name='delete_photo'),
    path("lessons/", views.LessonsView.as_view(), name='lessons'),
    path("lessons/<int:pk>/", views.LessonView.as_view(), name='lesson'),
    path("buy/", views.BuyView.as_view(), name='buy'),
]
