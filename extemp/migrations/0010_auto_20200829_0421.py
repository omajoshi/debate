# Generated by Django 3.1 on 2020-08-29 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extemp', '0009_section_open'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='open',
        ),
        migrations.AddField(
            model_name='round',
            name='open',
            field=models.BooleanField(default=False),
        ),
    ]