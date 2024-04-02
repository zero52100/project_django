from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .forms import SignupForm,LoginForm,ComplaintForm
from users.models import UserProfile 
from employeer.models import Job
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User, Group
from .models import Complaint

def homepage(request):
    job_listings = Job.objects.all()

    # Get filter values from the request
    employment_type = request.GET.get('employment_type')
    industry = request.GET.get('industry')
    location = request.GET.get('location')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort_by')

    # Apply filters to the job listings
    if employment_type:
        job_listings = job_listings.filter(employment_type=employment_type)
    if industry:
        job_listings = job_listings.filter(industry=industry)
    if location:
        job_listings = job_listings.filter(location=location)
    if search_query:
        job_listings = job_listings.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(company_name__company_name__icontains=search_query)
        )
    # Apply sorting to the job listings
    if sort_by == 'within_12_hours':
        job_listings = job_listings.filter(date_added__gte=timezone.now() - timedelta(hours=2))
    elif sort_by == 'within_24_hours':
        job_listings = job_listings.filter(date_added__gte=timezone.now() - timedelta(days=1))
    elif sort_by == 'within_7_days':
        job_listings = job_listings.filter(date_added__gte=timezone.now() - timedelta(days=7))
    elif sort_by == 'within_1_month':
        job_listings = job_listings.filter(date_added__gte=timezone.now() - timedelta(days=30))

    
    

    job_listings = job_listings.order_by('-id')

    return render(request, 'users/homepage.html', {'job_listings': job_listings})




def home1(request):
    job_listings = Job.objects.filter().order_by('-id')
    return render(request,'users/home.html',{'job_listings': job_listings})
    
def user_signup(request):
    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm() 
    return render(request,'users/signup.html' ,{'form':form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin1:admin1_home') # Redirect to admin homepage
                elif user.userprofile.user_type == 'employer':
                    return redirect('employeer:employeer_home')
                else:
                    return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm() 
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')
def complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.usertype=request.user.userprofile.user_type # Set the user field to the current user
            complaint.save()
            return redirect('home1')
    else:
        form = ComplaintForm()
    complaints = Complaint.objects.filter(user=request.user)
    
    return render(request, 'users/complaint.html', {'form': form, 'complaints': complaints})
def view_complaint(request):
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        if complaint_id:
            complaint = get_object_or_404(Complaint, pk=complaint_id)
            complaint.status = 'solved'
            complaint.save()
    complaints = Complaint.objects.all()
    return render(request, 'users/view_complaint.html', {'complaints': complaints})