from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import redirect


class AdminRequired(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CoursePurchaseRequired(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect('home')
        elif not user.is_course_purchased:
            return redirect('profile')
        else:
            return super().dispatch(request, *args, **kwargs)


class CourseNotPurchaseRequired(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated and user.is_course_purchased:
            return redirect('profile')
        else:
            return super().dispatch(request, *args, **kwargs)
