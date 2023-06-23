from django.contrib import admin

from .models import Lesson, Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["lesson", "resolution", "file"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    class VideoInline(admin.TabularInline):
        model = Video
        extra = 0
        can_delete = True
        show_change_link = True

    list_display = ["number", "is_published", "count_videos"]
    list_editable = ["is_published"]
    inlines = [VideoInline]
    ordering = ["number"]
    list_filter = ["is_published"]

    def count_videos(self, obj: Lesson):
        return obj.videos.count()

    def get_queryset(self, request):
        qs = super().get_queryset(request=request).prefetch_related("videos")
        return qs

    count_videos.short_description = "Количество видео"
