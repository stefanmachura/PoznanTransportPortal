# Generated by Django 2.2.3 on 2019-10-22 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikes', '0004_auto_20191022_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bikerack',
            name='updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]