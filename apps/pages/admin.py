from django.contrib import admin
from .models import FeedbackModel, FeedbackFileModel


@admin.register(FeedbackModel)
class FeedbackModelAdmin(admin.ModelAdmin):
    class FeedbackFileInline(admin.TabularInline):
        model = FeedbackFileModel
        extra = 0

        verbose_name = "файл"
        verbose_name_plural = "файлы"

        can_delete = False
        readonly_fields = ["file"]

    list_display = ["name", "email", "text", "count_files", "is_closed"]
    list_filter = ["is_closed"]

    inlines = [FeedbackFileInline]
    change_form_template = 'admin/feedback/change.html'

    def count_files(self, obj: FeedbackModel):
        return obj.files.count()

    def get_queryset(self, request):
        qs = super().get_queryset(request=request).prefetch_related("files")
        return qs

    def response_change(self, request, obj: FeedbackModel):
        if "_close_appeal" in request.POST:
            obj.is_closed = True
            obj.save()
            self.message_user(request, f"Обращение № {obj.id} успешно закрыто.")
        return super().response_change(request, obj)
