# Generated by Django 3.2.8 on 2021-12-02 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='qna',
            table='post_qna',
        ),
        migrations.AlterModelTable(
            name='qnaanswer',
            table='post_qna_answer',
        ),
        migrations.AlterModelTable(
            name='qnaanswercomment',
            table='post_qna_answer_comment',
        ),
        migrations.AlterModelTable(
            name='qnaanswercommentreply',
            table='post_qna_answer_comment_reply',
        ),
        migrations.AlterModelTable(
            name='qnaanswercount',
            table='post_qna_answer_count',
        ),
        migrations.AlterModelTable(
            name='qnacount',
            table='post_qna_count',
        ),
        migrations.AlterModelTable(
            name='qnapreview',
            table='post_qna_preview',
        ),
    ]
