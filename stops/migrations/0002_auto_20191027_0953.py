# Generated by Django 2.2.6 on 2019-10-27 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stop',
            name='lines',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='stop',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
