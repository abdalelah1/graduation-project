# Generated by Django 4.0.4 on 2023-11-23 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartadvisor', '0022_remove_advisor_email_remove_advisor_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommended_course',
            name='course',
        ),
        migrations.RemoveField(
            model_name='recommended_course',
            name='student',
        ),
        migrations.RemoveField(
            model_name='sublevel',
            name='level',
        ),
        migrations.RemoveField(
            model_name='course',
            name='level2',
        ),
        migrations.DeleteModel(
            name='level2',
        ),
        migrations.DeleteModel(
            name='Recommended_Course',
        ),
        migrations.DeleteModel(
            name='sublevel',
        ),
    ]
