# Generated by Django 4.1.7 on 2023-03-17 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0003_alter_book_book_alter_book_year_of_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book',
            field=models.FileField(default=None, max_length=250, null=True, upload_to='book/pdf'),
        ),
    ]