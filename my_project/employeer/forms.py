from django import forms
from users.models import UserProfile, Company

from .models import Job

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    company_name = forms.CharField(label='Company Name')
    company = Company.objects.first()  # Assuming there's always at least one company
    DESIGNATION_CHOICES = company.DESIGNATION_CHOICES

    designation = forms.ChoiceField(
        choices=DESIGNATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['email', 'designation','company_name']

class add_jobForm(forms.ModelForm):
    
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['company_name','user','user_email']
        
        user_type = forms.ChoiceField(
        choices=[('job_seeker', 'Job Seeker'), ('employer', 'Employer')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label='User Type'
    )
        widgets = {
            'application_deadline': forms.DateInput(attrs={'type': 'date'})
        }
class JobForm(forms.ModelForm):
    WORK_LOCATION_CHOICES = [
        ('hybrid', 'Hybrid'),
        ('work_from_home', 'Work from Home'),
        ('work_from_office', 'Work from Office'),
    ]
    
    employment_type = forms.ChoiceField(
        choices=WORK_LOCATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label='Work Location'
    )
    
    class Meta:
        model = Job
        fields = ['title', 'description', 'salary_range', 'application_deadline', 'location','required_qualifications','desired_qualifications','responsibilities'
                  ,'company_benefits','how_to_apply','other_information', 'employment_type']
    