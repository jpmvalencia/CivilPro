# Generated by Django 5.0.6 on 2024-09-24 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0002_task_incharge'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(default='Etapa Inicial', max_length=50),
        ),
    ]