# Generated by Django 2.2.3 on 2019-10-26 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departures', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='departure',
            options={'ordering': ['timestamp']},
        ),
        migrations.AlterUniqueTogether(
            name='departure',
            unique_together={('line', 'timestamp')},
        ),
        migrations.AddConstraint(
            model_name='departure',
            constraint=models.UniqueConstraint(fields=('line', 'timestamp'), name='unique_departure'),
        ),
    ]
