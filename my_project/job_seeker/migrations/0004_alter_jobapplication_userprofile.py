# Generated by Django 5.0.3 on 2024-04-01 01:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0003_jobapplication_userprofile_jobapplication_full_name'),
        ('users', '0005_alter_userprofile_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='UserProfile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile'),
        ),
    ]
