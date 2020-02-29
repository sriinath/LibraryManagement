# Generated by Django 2.2.10 on 2020-02-22 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_books_user_info'),
    ]

    operations = [
        migrations.RenameField(
            model_name='books',
            old_name='book_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='books',
            old_name='stock_count',
            new_name='stock',
        ),
        migrations.RenameField(
            model_name='books',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='books',
            name='user_info',
        ),
        migrations.AddField(
            model_name='books',
            name='price',
            field=models.FloatField(default=None, null=True),
        ),
    ]
