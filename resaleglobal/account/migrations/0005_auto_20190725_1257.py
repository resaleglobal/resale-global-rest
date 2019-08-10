# Generated by Django 2.2.2 on 2019-07-25 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20190725_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='consignor',
            name='address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='consignor',
            name='email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='consignor',
            name='number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userconsignorassignment',
            name='main_contact',
            field=models.BooleanField(default=True),
        ),
    ]