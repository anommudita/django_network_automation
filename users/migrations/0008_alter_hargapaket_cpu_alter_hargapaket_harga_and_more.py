# Generated by Django 4.2.5 on 2023-12-26 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_hargapaket_keterangan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hargapaket',
            name='cpu',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='hargapaket',
            name='harga',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='hargapaket',
            name='nama_paket',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='hargapaket',
            name='ram',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='hargapaket',
            name='storage',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
