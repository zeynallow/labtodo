# Generated by Django 2.2.3 on 2019-07-29 20:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0006_auto_20190729_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='due_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
