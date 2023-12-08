# Generated by Django 4.0.4 on 2023-11-22 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartadvisor', '0020_advisor'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='email',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='advisor',
            name='password',
            field=models.CharField(default='aaaa', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='advisor',
            name='department',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.department'),
        ),
    ]
