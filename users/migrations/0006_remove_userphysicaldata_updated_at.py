# Generated by Django 3.2.8 on 2021-12-06 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20211206_1723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userphysicaldata',
            name='updated_at',
        ),
    ]