# Generated by Django 4.2 on 2023-05-25 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_rename_addproblem_problem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_code', models.CharField(max_length=10000)),
            ],
        ),
    ]
