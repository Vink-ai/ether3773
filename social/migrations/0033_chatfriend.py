# Generated by Django 3.0.3 on 2020-04-20 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0032_auto_20200420_2212'),
    ]

    operations = [
        migrations.CreateModel(
            name='chatFriend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usr1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.profile')),
                ('usr2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
