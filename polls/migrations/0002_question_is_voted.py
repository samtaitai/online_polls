# Generated by Django 4.2.13 on 2024-06-21 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_voted',
            field=models.BooleanField(default=False),
        ),
    ]
