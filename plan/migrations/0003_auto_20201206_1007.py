# Generated by Django 2.2 on 2020-12-06 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0002_auto_20201206_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='store_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
