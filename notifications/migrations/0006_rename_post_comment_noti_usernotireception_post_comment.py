# Generated by Django 3.2.8 on 2022-04-17 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_rename_post_eply_usernotireception_post_reply'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usernotireception',
            old_name='post_comment_noti',
            new_name='post_comment',
        ),
    ]
