# Generated by Django 3.1.6 on 2021-04-28 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASISupport_app', '0012_auto_20210413_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='num_of_engineers',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
