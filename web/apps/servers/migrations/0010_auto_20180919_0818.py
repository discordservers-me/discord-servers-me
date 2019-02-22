# Generated by Django 2.1.1 on 2018-09-19 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0009_servertag_material_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='discordserver',
            name='premium_from',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='discordserver',
            name='premium_highlight',
            field=models.IntegerField(choices=[(0, 'Blue Grey'), (1, 'Indigo'), (2, 'Purple'), (3, 'Red')], default=0),
        ),
        migrations.AddField(
            model_name='discordserver',
            name='premium_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
