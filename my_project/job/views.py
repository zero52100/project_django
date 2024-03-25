from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from job.models import Job
from .forms import AddJobForm, ApplicationForm
from .models import Job,Application

from notification.utilities import create_notification

def search(request):
    return render(request, 'job/search.html')

def job_detail(request, job_id):
    job = Job.objects.get(pk=job_id)

    return render(request, 'job/job_detail.html', {'job': job})

def search_jobs(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        company_size = request.POST.get('company_size')
        work_mode = request.POST.get('work_mode')

        # Perform search based on the parameters
        jobs = Job.objects.filter(title__icontains=query)

        # Filter by company_size if provided
        if company_size:
            jobs = jobs.filter(company_size=company_size)

        # Filter by work_mode if provided
        if work_mode:
            jobs = jobs.filter(work_mode=work_mode)

        # Convert queryset to JSON format
        jobs_json = [{'id': job.id, 'title': job.title, 'company_name': job.company_name, 'url': job.get_absolute_url()} for job in jobs]

        return JsonResponse({'jobs': jobs_json})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
@login_required
def apply_for_job(request, job_id):
    job = Job.objects.get(pk=job_id)
    
    # Check if the user has already applied for this job
    user_has_applied = Application.objects.filter(job=job, created_by=request.user).exists()
    name = request.user.first_name + ' ' + request.user.last_name
    email = request.user.email
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.created_by = request.user
            application.save()
            # Handle notification and redirect as needed
            return redirect('dashboard')
    else:
        form = ApplicationForm(initial={'name': name, 'email': email})
    
    return render(request, 'job/apply_for_job.html', {'form': form, 'job': job, 'user_has_applied': user_has_applied})


@login_required
def add_job(request):
    if request.method == 'POST':
        form = AddJobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()

            return redirect('dashboard')
    else:
        form = AddJobForm()
    
    return render(request, 'job/add_job.html', {'form': form})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id, created_by=request.user)

    if request.method == 'POST':
        form = AddJobForm(request.POST, instance=job)

        if form.is_valid():
            job = form.save(commit=False)
            job.status = request.POST.get('status')
            job.save()

            return redirect('dashboard')
    else:
        form = AddJobForm(instance=job)
    
    return render(request, 'job/edit_job.html', {'form': form, 'job': job})