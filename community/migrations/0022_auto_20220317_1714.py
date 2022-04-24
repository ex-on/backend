# Generated by Django 3.2.8 on 2022-03-17 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0021_qnaanswercommentreplycount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qnaanswercommentcount',
            name='count_likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='qnaanswercommentcount',
            name='count_reports',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='qnaanswercommentreplycount',
            name='count_reports',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='qnaanswercount',
            name='count_comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='qnaanswercount',
            name='count_likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='qnaanswercount',
            name='count_reports',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='qnacount',
            name='count_answers',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='qnacount',
            name='count_comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='qnacount',
            name='count_likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='qnacount',
            name='count_reports',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='qnacount',
            name='count_saved',
            field=models.IntegerField(default=0),
        ),
    ]