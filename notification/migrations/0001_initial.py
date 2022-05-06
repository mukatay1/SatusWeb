# Generated by Django 4.0.3 on 2022-05-06 07:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.PositiveSmallIntegerField()),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_has_seen', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'NotificationModel',
                'verbose_name_plural': 'NotificationModel',
            },
        ),
    ]
