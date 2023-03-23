# Generated by Django 4.1.7 on 2023-03-17 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0002_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book',
            field=models.FileField(default=None, max_length=250, null=True, upload_to='media/book/pdf'),
        ),
        migrations.AlterField(
            model_name='book',
            name='year_of_published',
            field=models.IntegerField(null=True),
        ),
    ]