# Generated by Django 2.2.2 on 2019-09-05 23:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('reseller', '0004_auto_20190810_1018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemphotos',
            name='url',
        ),
        migrations.AddField(
            model_name='itemphotos',
            name='file_type',
            field=models.CharField(default='jpg', max_length=255),
        )
    ]
