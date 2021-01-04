# Generated by Django 3.1 on 2021-01-04 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_slot'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-day'], 'verbose_name': 'Scheduling', 'verbose_name_plural': 'Scheduling'},
        ),
        migrations.AlterField(
            model_name='slot',
            name='name',
            field=models.CharField(help_text='Morning or Evening', max_length=200, null=True),
        ),
    ]
