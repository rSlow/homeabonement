# Generated by Django 4.2 on 2023-06-25 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_paymentmodel_description_alter_paymentmodel_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentmodel',
            name='is_closed',
        ),
        migrations.AddField(
            model_name='paymentmodel',
            name='is_check_sent',
            field=models.BooleanField(default=False, verbose_name='Чек отправлен'),
        ),
    ]
