# Generated by Django 3.1 on 2020-08-27 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extemp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='running_index',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='topicinstance',
            name='index',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
