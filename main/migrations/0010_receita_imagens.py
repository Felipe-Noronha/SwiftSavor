# Generated by Django 5.0.1 on 2024-01-31 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_receita_data_cadastro'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='imagens',
            field=models.ImageField(blank=True, null=True, upload_to='receitas/'),
        ),
    ]