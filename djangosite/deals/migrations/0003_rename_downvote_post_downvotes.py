# Generated by Django 5.1.1 on 2024-09-28 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0002_rename_score_post_downvote_post_upvotes_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='downvote',
            new_name='downvotes',
        ),
    ]
