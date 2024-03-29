# Generated by Django 5.0.1 on 2024-02-03 14:49

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingredients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Receita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('instrucoes', models.TextField()),
                ('data_cadastro', models.DateField(default=django.utils.timezone.now)),
                ('ingredientes', models.ManyToManyField(to='ingredients.ingrediente')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ImagemReceita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='receitas/')),
                ('receita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagens_receita', to='recipes.receita')),
            ],
        ),
        migrations.CreateModel(
            name='ReceitaFavorita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.receita')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('usuario', 'receita')},
            },
        ),
    ]
