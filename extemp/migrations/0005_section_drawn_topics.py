# Generated by Django 3.1 on 2020-08-28 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extemp', '0004_round_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='drawn_topics',
            field=models.ManyToManyField(related_name='sections_drawn', to='extemp.TopicInstance'),
        ),
    ]