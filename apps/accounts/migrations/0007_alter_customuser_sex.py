# Generated by Django 4.2 on 2023-06-23 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_is_course_purchased'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='sex',
            field=models.CharField(blank=True, choices=[('W', 'Женский'), ('M', 'Мужской')], max_length=1, null=True, verbose_name='Пол'),
        ),
    ]
