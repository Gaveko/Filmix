# Generated by Django 3.0.2 on 2021-08-16 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cinema', '0013_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='stars',
        ),
    ]
