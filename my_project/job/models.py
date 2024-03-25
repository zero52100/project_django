from django.contrib.auth.models import User
from django.db import models
from django import forms


class Job(models.Model):
    SIZE_1_9 = 'size_1-9'
    SIZE_10_49 = 'size_10-49'
    SIZE_50_99 = 'size_50-99'
    SIZE_100 = 'size_100'

    CHOICES_SIZE = (
        (SIZE_1_9, '1-3'),
        (SIZE_10_49, '3-6'),
        (SIZE_50_99, '6-10'),
        (SIZE_100, '10+'),
    )
    WORK_MODE_OFFICE = 'office'
    WORK_MODE_HOME = 'home'
    WORK_MODE_HYBRID = 'hybrid'

    CHOICES_WORK_MODE = (
        (WORK_MODE_OFFICE, 'Office'),
        (WORK_MODE_HOME, 'Home'),
        (WORK_MODE_HYBRID, 'Hybrid'),
    )

    ACTIVE = 'active'
    EMPLOYED = 'employed'
    ARCHIVED = 'archived'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (EMPLOYED, 'Employed'),
        (ARCHIVED, 'Archived')
    )

    title = models.CharField(max_length=255)
    short_description = models.TextField()
    long_description = models.TextField(blank=True, null=True)
    long_description1 = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    company_zipcode = models.CharField(max_length=255, blank=True, null=True)
    company_place = models.CharField(max_length=255, blank=True, null=True)
    company_country = models.CharField(max_length=255, blank=True, null=True)
    company_size = models.CharField(max_length=20, choices=CHOICES_SIZE, default=SIZE_1_9)
    work_mode = models.CharField(max_length=10, choices=CHOICES_WORK_MODE,default=WORK_MODE_OFFICE)
    created_by = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=ACTIVE)
    deadline = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE)
    content = models.TextField()
    experience = models.TextField()

    created_by = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['content', 'experience', 'name', 'email', 'resume']

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    resume = forms.FileField()