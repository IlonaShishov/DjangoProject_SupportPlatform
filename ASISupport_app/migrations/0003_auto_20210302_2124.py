# Generated by Django 3.1.6 on 2021-03-02 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASISupport_app', '0002_auto_20210302_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='on_hold',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='role',
        ),
        migrations.AlterField(
            model_name='case',
            name='cancellation_reason',
            field=models.TextField(blank=True),
        ),
    ]