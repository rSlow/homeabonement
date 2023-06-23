from pathlib import Path

from django.core.validators import FileExtensionValidator
from django.db import models


class PublishedLessonsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class Lesson(models.Model):
    number = models.IntegerField(
        verbose_name="Номер урока",
    )
    thumbnail = models.ImageField(
        verbose_name="Обложка видео",
        upload_to="lessons/thumbnails",
        null=True,
        blank=True
    )
    is_published = models.BooleanField(
        verbose_name="Опубликован",
        default=False,
    )

    objects = models.Manager()
    published = PublishedLessonsManager()

    def __str__(self):
        return f"Урок № {self.number}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Video(models.Model):
    resolution = models.IntegerField(
        verbose_name="Разрешение видео",
    )
    file = models.FileField(
        verbose_name="Видео",
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
        upload_to='lessons/videos'
    )
    lesson = models.ForeignKey(
        to=Lesson,
        on_delete=models.CASCADE,
        verbose_name="Урок",
        related_name="videos"
    )

    def __str__(self):
        file_path = Path(self.file.name)
        return f"Видео {file_path.parts[-1]} <{self.resolution}p>"

    class Meta:
        verbose_name = "видео"
        verbose_name_plural = "видео"
