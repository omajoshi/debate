# Generated by Django 3.1 on 2020-08-28 20:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('extemp', '0005_section_drawn_topics'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='sections_in', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='section',
            name='drawn_topics',
            field=models.ManyToManyField(blank=True, related_name='sections_drawn', to='extemp.TopicInstance'),
        ),
    ]
