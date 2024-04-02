from django import forms
from .models import UserProfile  # Remove this line
from .models import JobApplication
class ProfileForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=100,
        required=True,
        help_text='Enter Email Address',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )

    class Meta:
        model = UserProfile
        fields = ['email', 'cover_letter', 'resume']



class JobApplicationForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=100,
        required=True,  
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    
    class Meta:
        model = JobApplication
        fields = ['full_name','username', 'email', 'resume', 'cover_letter']
