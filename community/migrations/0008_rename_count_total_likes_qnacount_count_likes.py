# Generated by Django 3.2.8 on 2021-12-21 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0007_auto_20211220_2058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qnacount',
            old_name='count_total_likes',
            new_name='count_likes',
        ),
    ]