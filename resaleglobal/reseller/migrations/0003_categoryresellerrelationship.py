# Generated by Django 2.2.2 on 2019-07-29 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20190725_1257'),
        ('reseller', '0002_auto_20190726_1229'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryResellerRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reseller.Category')),
                ('reseller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Reseller')),
            ],
        ),
    ]
