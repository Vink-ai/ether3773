# Generated by Django 3.0.3 on 2020-04-09 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_profile_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
