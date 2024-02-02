# Generated by Django 5.0.1 on 2024-01-31 23:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_receita_imagens'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receita',
            name='imagens',
        ),
        migrations.CreateModel(
            name='ImagemReceita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='receitas/')),
                ('receita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagens_receita', to='main.receita')),
            ],
        ),
    ]