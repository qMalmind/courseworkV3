# Generated by Django 3.2.9 on 2021-11-23 16:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('kyrsah', '0002_auto_20211123_2110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='idRole',
        ),
        migrations.AlterField(
            model_name='article',
            name='dateCreate',
            field=models.TimeField(default=datetime.datetime(2021, 11, 23, 16, 22, 26, 343502, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='dateRegistration',
            field=models.TimeField(default=datetime.datetime(2021, 11, 23, 16, 22, 26, 342502, tzinfo=utc)),
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]