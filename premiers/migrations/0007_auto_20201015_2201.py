# Generated by Django 3.1 on 2020-10-15 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('premiers', '0006_mainpurpose_subpurpose'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpurpose',
            name='main_weight',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='subpurpose',
            name='sub_weight',
            field=models.FloatField(null=True),
        ),
    ]
