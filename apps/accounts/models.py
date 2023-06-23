from io import BytesIO
from pathlib import Path

from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from phonenumber_field.modelfields import PhoneNumberField

SexChoices = [
    ("W", "Женский"),
    ("M", "Мужской"),
]


class CustomUser(AbstractUser):
    photo = models.ImageField(
        upload_to='profile_pic',
        verbose_name="Фото профиля",
        null=True,
        blank=True,
    )
    sex = models.CharField(
        max_length=1,
        choices=SexChoices,
        verbose_name="Пол",
        null=True,
        blank=True,
    )
    phone = PhoneNumberField(
        verbose_name="Номер телефона",
        null=True,
        blank=True,
        region="RU",
    )
    is_course_purchased = models.BooleanField(
        verbose_name="Оплата курса",
        default=False,
        help_text="Отметьте, если курс был оплачен."
    )

    def __str__(self):
        return self.email

    @staticmethod
    def compress(image_file: "ImageFieldFile"):
        pillow_image = Image.open(image_file)
        pillow_image = pillow_image.convert('RGBA')

        size_x, size_y = pillow_image.size
        img_width, img_height = pillow_image.size
        crop_size = min(size_x, size_y)
        pillow_image = pillow_image.crop((
            (img_width - crop_size) // 2,
            (img_height - crop_size) // 2,
            (img_width + crop_size) // 2,
            (img_height + crop_size) // 2)
        )

        image_io = BytesIO()
        pillow_image.save(image_io, 'PNG', quality=70)

        file_path = Path(image_file.name)
        new_image_file = ContentFile(image_io.getvalue(), name=file_path.name)

        return new_image_file

    def save(self, *args, **kwargs):
        if self.photo and self.photo._committed is False:
            self.photo = self.compress(self.photo)
        super().save(*args, **kwargs)
