# Generated by Django 3.0.2 on 2021-08-16 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cinema', '0011_film_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='url',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
