# Generated by Django 3.2.8 on 2022-04-17 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20220417_0004'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usernotireception',
            old_name='post_eply',
            new_name='post_reply',
        ),
    ]
