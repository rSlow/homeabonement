# Generated by Django 4.2 on 2023-06-05 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': 'Урок', 'verbose_name_plural': 'Уроки'},
        ),
        migrations.AddField(
            model_name='lesson',
            name='text',
            field=models.TextField(null=True, verbose_name='Описание урока'),
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]
