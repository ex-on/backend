# Generated by Django 3.2.8 on 2021-12-21 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0010_alter_qna_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qnacount',
            old_name='count_total_comments',
            new_name='count_comments',
        ),
    ]
