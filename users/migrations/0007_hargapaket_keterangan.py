# Generated by Django 4.2.5 on 2023-12-21 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_hargapaket_perbulan_remove_pesanan_keterangan_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hargapaket',
            name='keterangan',
            field=models.TextField(null=True),
        ),
    ]
