from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from job.models import Job
from userprofile.models import Userprofile
from .forms import CustomUserCreationForm 
from django.contrib.auth.decorators import user_passes_test
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    # Retrieve required information
    total_jobs = Job.objects.count()
    total_employers = Userprofile.objects.filter(is_employer=True).count()
    total_employees = Userprofile.objects.filter(is_employer=False).count()

    return render(request, 'core/admin_dashboard.html', {
        'total_jobs': total_jobs,
        'total_employers': total_employers,
        'total_employees': total_employees,
    })
def frontpage(request):
    jobs = Job.objects.filter(status=Job.ACTIVE).order_by('-created_at')[0:3]

    return render(request, 'core/frontpage.html', {'jobs': jobs})
def custom_logout(request):
    if request.method == 'POST' or request.method == 'GET':
        auth_logout(request)
        return redirect('frontpage')
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use the custom user creation form

        if form.is_valid():
            user = form.save()

            account_type = request.POST.get('account_type', 'jobseeker')

            if account_type == 'employer':
                userprofile = Userprofile.objects.create(user=user, is_employer=True)
                userprofile.save()
            else:
                userprofile = Userprofile.objects.create(user=user)
                userprofile.save()

            login(request, user)

            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()  # Use the custom user creation form

    return render(request, 'core/signup.html', {'form': form})