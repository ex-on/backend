# Generated by Django 3.2.8 on 2021-12-20 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0007_auto_20211220_2058'),
        ('users', '0008_auto_20211215_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetailscount',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userdetailsstatic',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userphysicaldata',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userssavedposts',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.post'),
        ),
        migrations.AlterField(
            model_name='userssavedposts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userssavedqnaposts',
            name='qna_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.qna'),
        ),
        migrations.AlterField(
            model_name='userssavedqnaposts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
