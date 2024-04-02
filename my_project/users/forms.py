from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Complaint

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100,
        required=True,
        help_text='Enter Email Address',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    user_type = forms.ChoiceField(
        choices=[('job_seeker', 'Job Seeker'), ('employer', 'Employer')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label='User Type'
    )
    full_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User  
        fields = ['full_name','username', 'email', 'password1', 'password2', 'user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_profile = UserProfile.objects.create(user=user, user_type=self.cleaned_data['user_type'], full_name=self.cleaned_data['full_name']) 
            user_profile.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()    
    password = forms.CharField(widget=forms.PasswordInput)

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['complaint_type', 'message']
        widgets = {
            'complaint_type': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }