# Generated by Django 3.2.8 on 2022-03-01 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0018_auto_20220225_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qna',
            name='solved',
            field=models.BooleanField(default=False),
        ),
    ]
