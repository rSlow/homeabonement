from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from apps.accounts.forms import CustomUserChangeForm
from apps.accounts.models import CustomUser
from config.permissions import CoursePurchaseRequired, CourseNotPurchaseRequired
from .models import Lesson


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'courses/profile.html'
    form_class = CustomUserChangeForm
    model = CustomUser

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        if form.changed_data:
            messages.add_message(
                request=self.request,
                level=messages.SUCCESS,
                message="Изменения профиля сохранены."
            )
        else:
            messages.add_message(
                request=self.request,
                level=messages.INFO,
                message="Не было внесено изменений."
            )
        return super().form_valid(form=form)


class RemoveProfilePhoto(View):
    http_method_names = ["get"]

    def get(self, request):
        user: CustomUser = self.request.user
        user.photo.delete()
        user.save()

        return redirect('profile')


class LessonsView(CoursePurchaseRequired, ListView):
    model = Lesson
    template_name = 'courses/lessons.html'

    def get_queryset(self):
        queryset = self.model.published.order_by("number")
        return queryset


class LessonView(CoursePurchaseRequired, DetailView):
    model = Lesson
    template_name = 'courses/lesson.html'

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']
        return self.model.published.prefetch_related("videos").get(pk=pk)


class BuyView(CourseNotPurchaseRequired, TemplateView):
    template_name = 'courses/buy.html'
