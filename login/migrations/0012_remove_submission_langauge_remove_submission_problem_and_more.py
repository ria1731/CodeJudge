# Generated by Django 4.2 on 2023-07-17 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='langauge',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='problem',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='submission_time',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='user',
        ),
        migrations.DeleteModel(
            name='TestCases',
        ),
    ]
