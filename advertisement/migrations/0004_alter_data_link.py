# Generated by Django 4.1.3 on 2022-11-30 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("advertisement", "0003_alter_data_pricewithoutfees"),
    ]

    operations = [
        migrations.AlterField(
            model_name="data",
            name="link",
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
