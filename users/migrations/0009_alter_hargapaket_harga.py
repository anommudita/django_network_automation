# Generated by Django 4.2.5 on 2023-12-26 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_hargapaket_cpu_alter_hargapaket_harga_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hargapaket',
            name='harga',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
