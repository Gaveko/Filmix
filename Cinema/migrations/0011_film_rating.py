# Generated by Django 3.0.2 on 2021-08-14 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cinema', '0010_auto_20210814_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
