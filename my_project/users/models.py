from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=[('job_seeker', 'Job Seeker'), ('employer', 'Employer')])
    cover_letter = models.TextField(blank=True)  # Field to store the cover letter
    resume = models.FileField(upload_to='resumes/', blank=True)  # Field to upload the resume file
    full_name = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        
        if self.user_type == 'employer':
            # If the user is an employer, create a corresponding Company entry
            company, created = Company.objects.get_or_create(user=self.user)
        super().save(*args, **kwargs)

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    company_website = models.URLField(blank=True)
    DESIGNATION_CHOICES = [
        ('hr', 'HR'),
        ('manager', 'Manager'),
        ('ceo', 'CEO')
    ]
    designation = models.CharField(max_length=20, choices=DESIGNATION_CHOICES, default='hr')

    def __str__(self):
        return self.company_name
class Complaint(models.Model):
    COMPLAINT_TYPES = [
        ('account_related', 'Account Related'),
        ('job_related', 'Job Related'),
        ('employer_related', 'Complaint Against Employer'),
        ('user_related', 'Complaint Against User'),
        
    ]
    COMPLAINT_STATUS = [
        ('awaiting', 'Awaiting'),
        ('solved', 'Solved'),
        
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=[('job_seeker', 'Job Seeker'), ('employer', 'Employer')])
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPES)
    status = models.CharField(max_length=20, choices=COMPLAINT_STATUS, default='awaiting')
    message = models.TextField()

    def __str__(self):
        return f"Complaint from {self.user.username}"



