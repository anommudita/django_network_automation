# Generated by Django 4.2.5 on 2023-12-21 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_hargapaket_perbulan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hargapaket',
            name='perbulan',
        ),
        migrations.RemoveField(
            model_name='pesanan',
            name='keterangan',
        ),
        migrations.AddField(
            model_name='pesanan',
            name='perbulan',
            field=models.CharField(max_length=100, null=True),
        ),
    ]