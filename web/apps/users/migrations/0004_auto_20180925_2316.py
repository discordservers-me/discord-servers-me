# Generated by Django 2.1.1 on 2018-09-25 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180925_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='discord_email',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
