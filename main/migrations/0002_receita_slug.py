# Generated by Django 5.0.1 on 2024-01-28 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]
