from django.core.validators import MinLengthValidator
from django.db import models


class FeedbackModel(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Имя"
    )
    email = models.EmailField(
        verbose_name="Электронная почта"
    )
    text = models.TextField(
        verbose_name="Сообщение",
        help_text="не менее 20 символов",
        validators=[MinLengthValidator(limit_value=20)]
    )
    is_closed = models.BooleanField(
        verbose_name="Закрыто",
        default=False,
        help_text="Отметьте, если рассмотрение обращения закончено."
    )

    def __str__(self):
        return f"Обращение №{self.pk} от {self.email}"

    class Meta:
        verbose_name = "обращение"
        verbose_name_plural = "обращения"


class FeedbackFileModel(models.Model):
    file = models.FileField(
        verbose_name="Файл",
        upload_to="feedback/"
    )
    feedback = models.ForeignKey(
        to="pages.FeedbackModel",
        on_delete=models.CASCADE,
        verbose_name="Отзыв",
        related_name="files"
    )

    def __str__(self):
        return f"{self.file.name}"
