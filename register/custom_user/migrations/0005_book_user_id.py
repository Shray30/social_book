# Generated by Django 4.1.7 on 2023-03-20 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0004_alter_book_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='user_id',
            field=models.IntegerField(default=None),
        ),
    ]
