# Generated by Django 3.2.8 on 2022-04-08 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_userdetailsstatic_fcm_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetailscount',
            name='answer_acception_rate',
        ),
    ]
