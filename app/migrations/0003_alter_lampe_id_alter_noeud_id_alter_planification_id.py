# Generated by Django 5.0.3 on 2024-03-27 09:20

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_lampe_id_alter_noeud_id_planification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lampe',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=22, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='noeud',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=22, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='planification',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=22, primary_key=True, serialize=False),
        ),
    ]