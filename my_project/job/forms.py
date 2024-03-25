from django import forms

from .models import Job, Application

class AddJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'short_description', 'long_description','long_description1', 'company_name', 'company_address', 'company_zipcode', 'company_place', 'company_country', 'company_size','work_mode','deadline']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['content', 'experience']