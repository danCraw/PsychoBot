# Generated by Django 4.0.6 on 2022-07-19 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('psychoapp', '0004_time_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='psycho',
        ),
    ]