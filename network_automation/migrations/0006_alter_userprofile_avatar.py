# Generated by Django 4.2.5 on 2023-10-19 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network_automation', '0005_userprofile_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]