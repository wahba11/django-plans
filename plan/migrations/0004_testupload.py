# Generated by Django 2.2 on 2020-12-06 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0003_auto_20201206_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
            ],
        ),
    ]
