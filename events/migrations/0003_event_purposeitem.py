# Generated by Django 3.1 on 2021-01-02 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('premiers', '0030_auto_20201228_2310'),
        ('events', '0002_event_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='purposeitem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='premiers.purposedetail'),
        ),
    ]
