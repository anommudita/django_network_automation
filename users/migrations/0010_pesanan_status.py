# Generated by Django 4.2.5 on 2023-12-26 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_hargapaket_harga'),
    ]

    operations = [
        migrations.AddField(
            model_name='pesanan',
            name='status',
            field=models.CharField(default='0', max_length=100, null=True),
        ),
    ]
