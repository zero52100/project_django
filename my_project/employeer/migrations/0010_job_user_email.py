# Generated by Django 5.0.3 on 2024-04-02 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeer', '0009_job_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='user_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
