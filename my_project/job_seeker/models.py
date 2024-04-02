from django import forms
from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile
from employeer.models import Job

class JobApplication(models.Model):
    
    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    UserProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    cover_letter = models.TextField()
    full_name = models.CharField(max_length=255) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='APPLIED')

    def __str__(self):
        return f"{self.user.username} - {self.job.title} -{self.full_name} - {self.get_status_display()}-"