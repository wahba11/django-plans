# Generated by Django 2.2 on 2020-12-06 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0004_testupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='testupload',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]