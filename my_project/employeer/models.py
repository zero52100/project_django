from django.db import models
from django.contrib.auth.models import User 
from users.models import Company
from django.utils import timezone
class Job(models.Model):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_email = models.EmailField(blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    required_qualifications = models.TextField()
    desired_qualifications = models.TextField()
    responsibilities = models.TextField()
    application_deadline = models.DateField()
    salary_range = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=timezone.now)
    employment_type = models.CharField(max_length=20, choices=[('work_from_home', 'Work From Home'), ('work_from_office', 'Work From Office'), ('hybrid', 'Hybrid')])
    company_benefits = models.TextField()
    how_to_apply = models.TextField()
    other_information = models.TextField()
    industry_type = [
        ('IT', 'Information Technology'),
        ('Healthcare', 'Healthcare'),
        ('Finance', 'Finance'),
        ('Education', 'Education'),
        ('Manufacturing', 'Manufacturing'),
    ]
    industry = models.CharField(max_length=20, choices=industry_type,default='IT')
    def save(self, *args, **kwargs):
        if self.user:
            self.user_email = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name