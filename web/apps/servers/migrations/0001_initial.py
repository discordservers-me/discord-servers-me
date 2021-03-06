# Generated by Django 2.1.1 on 2018-09-16 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiscordEmoji',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emoji_id', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField(blank=True)),
                ('require_colons', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DiscordServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_id', models.CharField(max_length=20)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('creation_date', models.DateTimeField(blank=True, null=True)),
                ('member_count', models.IntegerField(blank=True, null=True)),
                ('icon_url', models.URLField(blank=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='server_icons')),
                ('owner_id', models.CharField(blank=True, max_length=20)),
                ('premium_tier', models.IntegerField(blank=True, null=True)),
                ('short_description', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField(blank=True, max_length=2000)),
                ('shown', models.BooleanField(default=False)),
                ('bumped_at', models.DateTimeField(auto_now_add=True)),
                ('invite_link', models.URLField(blank=True)),
                ('website', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServerCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('servers', models.ManyToManyField(related_name='categories', to='servers.DiscordServer')),
            ],
        ),
        migrations.CreateModel(
            name='ServerTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('servers', models.ManyToManyField(related_name='tags', to='servers.DiscordServer')),
            ],
        ),
        migrations.AddField(
            model_name='discordemoji',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emojis', to='servers.DiscordServer'),
        ),
    ]
