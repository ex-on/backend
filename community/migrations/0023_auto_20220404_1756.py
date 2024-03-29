# Generated by Django 3.2.8 on 2022-04-04 17:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0022_auto_20220317_1714'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usersreportedpostcommentreplies',
            old_name='reply',
            new_name='post_comment_reply',
        ),
        migrations.RenameField(
            model_name='usersreportedpostcomments',
            old_name='comment',
            new_name='post_comment',
        ),
        migrations.RenameField(
            model_name='usersreportedqnaanswercommentreplies',
            old_name='reply',
            new_name='qna_answer_comment_reply',
        ),
        migrations.RenameField(
            model_name='usersreportedqnaanswercomments',
            old_name='comment',
            new_name='qna_answer_comment',
        ),
        migrations.RenameField(
            model_name='usersreportedqnaanswers',
            old_name='answer',
            new_name='qna_answer',
        ),
        migrations.AlterUniqueTogether(
            name='usersreportedpostcommentreplies',
            unique_together={('user', 'post_comment_reply')},
        ),
        migrations.AlterUniqueTogether(
            name='usersreportedpostcomments',
            unique_together={('user', 'post_comment')},
        ),
        migrations.AlterUniqueTogether(
            name='usersreportedqnaanswercommentreplies',
            unique_together={('user', 'qna_answer_comment_reply')},
        ),
        migrations.AlterUniqueTogether(
            name='usersreportedqnaanswercomments',
            unique_together={('user', 'qna_answer_comment')},
        ),
        migrations.AlterUniqueTogether(
            name='usersreportedqnaanswers',
            unique_together={('user', 'qna_answer')},
        ),
    ]
