# Generated by Django 4.0.6 on 2022-07-24 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_guest_reserve_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guest',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='guest',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='reserve_time',
            field=models.DateTimeField(),
        ),
    ]
