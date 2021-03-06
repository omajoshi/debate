# Generated by Django 3.1 on 2020-08-25 04:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='extemp.event')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='extemp.round')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('question', models.CharField(max_length=200)),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='extemp.round')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TopicInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField(default=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='extemp.section')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='extemp.topic')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='extemp.tournament'),
        ),
    ]
