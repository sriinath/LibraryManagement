# Generated by Django 2.2.10 on 2020-02-22 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='user_id',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='users',
            name='books_info',
        ),
    ]
