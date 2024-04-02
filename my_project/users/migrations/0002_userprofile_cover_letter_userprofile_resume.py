# Generated by Django 5.0.3 on 2024-03-26 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cover_letter',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='resume',
            field=models.FileField(blank=True, upload_to='resumes/'),
        ),
    ]