# Generated by Django 2.2.5 on 2021-04-16 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0005_merge_20210415_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='value_history',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
