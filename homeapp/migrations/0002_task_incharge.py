# Generated by Django 5.0.6 on 2024-09-24 02:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentapp', '0001_initial'),
        ('homeapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='inCharge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentapp.employee'),
        ),
    ]
