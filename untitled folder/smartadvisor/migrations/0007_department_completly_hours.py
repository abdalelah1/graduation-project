# Generated by Django 4.0.4 on 2023-10-25 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartadvisor', '0006_level_semester_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='completly_hours',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
