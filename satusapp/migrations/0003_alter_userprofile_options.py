# Generated by Django 4.0.3 on 2022-05-03 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satusapp', '0002_alter_comment_options_alter_message_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'UserProfile', 'verbose_name_plural': 'UserProfile'},
        ),
    ]
