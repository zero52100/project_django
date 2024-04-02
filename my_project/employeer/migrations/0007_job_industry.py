# Generated by Django 5.0.3 on 2024-03-31 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeer', '0006_job_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='industry',
            field=models.CharField(choices=[('IT', 'Information Technology'), ('Healthcare', 'Healthcare'), ('Finance', 'Finance'), ('Education', 'Education'), ('Manufacturing', 'Manufacturing')], default='IT', max_length=20),
        ),
    ]
