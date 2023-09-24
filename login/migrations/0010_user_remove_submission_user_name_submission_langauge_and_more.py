# Generated by Django 4.2 on 2023-07-17 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_alter_submission_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=20)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='submission',
            name='user_name',
        ),
        migrations.AddField(
            model_name='submission',
            name='langauge',
            field=models.CharField(default='C++', max_length=50),
        ),
        migrations.AddField(
            model_name='submission',
            name='problem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='login.problem'),
        ),
        migrations.AddField(
            model_name='submission',
            name='submission_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='user_code',
            field=models.CharField(default='FAILED', max_length=50),
        ),
        migrations.CreateModel(
            name='TestCases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.TextField()),
                ('output', models.TextField()),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.problem')),
            ],
        ),
    ]