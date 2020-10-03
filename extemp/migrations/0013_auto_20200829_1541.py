# Generated by Django 3.1 on 2020-08-29 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('extemp', '0012_auto_20200829_0512'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoundGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='round',
            name='roundgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='extemp.roundgroup'),
        ),
    ]
