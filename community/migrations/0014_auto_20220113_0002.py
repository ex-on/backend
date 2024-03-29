# Generated by Django 3.2.8 on 2022-01-12 15:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0013_auto_20211223_2352'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcomment',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='postcommentreply',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='postcount',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='qna',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='qnaanswer',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='qnaanswercomment',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='qnaanswercommentreply',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='qnacount',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='qnapreview',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='usersreportedpostcommentreplies',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='usersreportedpostcomments',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='usersreportedposts',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='usersreportedqnaanswercommentreplies',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='usersreportedqnaanswercomments',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='usersreportedqnaanswers',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='usersreportedqnas',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='post',
            name='creation_date',
        ),
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
