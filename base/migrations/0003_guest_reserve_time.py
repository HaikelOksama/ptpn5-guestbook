# Generated by Django 4.0.6 on 2022-07-20 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_guest_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='reserve_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
