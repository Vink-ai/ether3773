# Generated by Django 3.0.3 on 2020-04-13 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0021_auto_20200413_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
