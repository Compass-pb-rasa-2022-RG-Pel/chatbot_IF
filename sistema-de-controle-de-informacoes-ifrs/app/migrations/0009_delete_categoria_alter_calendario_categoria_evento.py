# Generated by Django 4.0.6 on 2022-07-23 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0002_alter_categorias_nome_categoria'),
        ('app', '0008_alter_calendario_imagem_evento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendario',
            name='categoria_evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categorias.categorias'),
        ),
    ]
