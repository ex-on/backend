# Generated by Django 3.2.8 on 2022-02-24 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0016_auto_20220113_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qna',
            name='type',
        ),
    ]
