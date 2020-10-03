# Generated by Django 3.1 on 2020-08-29 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extemp', '0014_roundgroup_tournament'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='roundgroup',
        ),
        migrations.AddField(
            model_name='roundgroup',
            name='rounds',
            field=models.ManyToManyField(blank=True, to='extemp.Round'),
        ),
    ]
