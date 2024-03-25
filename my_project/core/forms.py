from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, label='Full Name')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    gender = forms.ChoiceField(choices=(('male', 'Male'), ('female', 'Female')), label='Gender')
    company_name = forms.CharField(max_length=150, label='Company Name', required=False)
    designation = forms.ChoiceField(choices=(('hr', 'HR'), ('ceo', 'CEO'), ('manager', 'Manager')), label='Designation', required=False)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'password1', 'password2', 'gender', 'company_name', 'designation')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('full_name').split(' ')[0]  
        user.last_name = ' '.join(self.cleaned_data.get('full_name').split(' ')[1:])  
        user.email = self.cleaned_data.get('email')
        user.save()

        
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.company_name = self.cleaned_data.get('company_name')
        profile.designation = self.cleaned_data.get('designation')
        profile.gender = self.cleaned_data.get('gender')
        profile.save()

        return user
