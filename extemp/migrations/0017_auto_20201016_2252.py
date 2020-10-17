# Generated by Django 3.1 on 2020-10-17 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extemp', '0016_auto_20200829_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='code',
        ),
        migrations.AlterField(
            model_name='round',
            name='name',
            field=models.CharField(choices=[('1', 'Round 1'), ('2', 'Round 2'), ('3', 'Round 3'), ('4', 'Round 4'), ('5', 'Round 5'), ('6', 'Round 6'), ('7', 'Round 7'), ('8', 'Round 8'), ('9', 'Round 9'), ('d', 'Doubles'), ('o', 'Octas'), ('q', 'Quarters'), ('s', 'Semis'), ('f', 'Finals')], max_length=1),
        ),
    ]