# Generated by Django 2.2 on 2020-12-06 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0007_auto_20201206_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='change_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
