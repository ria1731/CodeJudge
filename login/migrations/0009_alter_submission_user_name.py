# Generated by Django 4.2 on 2023-05-31 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_remove_submission_user_submission_user_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='user_name',
            field=models.CharField(max_length=100),
        ),
    ]