# Generated by Django 3.2.8 on 2022-02-26 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0018_auto_20220225_1757'),
        ('users', '0021_auto_20220216_1704'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UsersSavedPosts',
            new_name='UsersBookmarkedPosts',
        ),
        migrations.RenameModel(
            old_name='UsersSavedQnas',
            new_name='UsersBookmarkedQnas',
        ),
        migrations.AlterModelTable(
            name='usersbookmarkedposts',
            table='users_bookmarked_posts',
        ),
        migrations.AlterModelTable(
            name='usersbookmarkedqnas',
            table='users_bookmarked_qnas',
        ),
    ]
