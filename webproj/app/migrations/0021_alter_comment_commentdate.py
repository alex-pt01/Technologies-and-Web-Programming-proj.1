# Generated by Django 3.2 on 2021-04-25 16:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20210425_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commentDate',
            field=models.DateField(default=datetime.datetime(2021, 4, 25, 17, 22, 28, 26017)),
        ),
    ]
