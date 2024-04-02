from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .forms import add_jobForm
from .models import Job
from django.db.models import Q
from job_seeker.models import JobApplication
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponseServerError
from .forms import JobForm
@login_required
def employeer_profile(request):
    employeer = request.user
    user_email = request.user.email
    user_type = request.user.userprofile.user_type
    company_name = request.user.company.company_name
    designation = request.user.company.designation

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            employeer.email = form.cleaned_data['email']
            employeer.save()

            # Update designation for the associated company
            company = request.user.company
            company.company_name=form.cleaned_data['company_name']
            company.designation = form.cleaned_data['designation']
            company.save()
            form.save()
            return redirect('employeer:employeer_profile')
    else:
        form = ProfileForm(instance=request.user.userprofile, initial={'email': user_email, 'designation': designation,'company_name':company_name})

    return render(request, 'employeer/employeer_profile.html', {
        'employeer': employeer,
        'user_email': user_email,
        'user_type': user_type,
        'form': form,
        'company_name': company_name,
        'designation': designation
    })
def add_job(request):
    company_name = request.user.company
    user = request.user 
    user_email = request.user.email
    if request.method == 'POST':
        form = add_jobForm(request.POST)
        if form.is_valid():
            job_listing = form.save(commit=False)
            job_listing.company_name = company_name 
            job_listing.user = user
            job_listing.user_email = user_email 
            job_listing.save()
            return redirect('employeer:add_job')
    else:
        form = add_jobForm()
    return render(request, 'employeer/add_job.html', {'form': form, 'company_name': company_name,'user': user,'user_email':user_email})

   
def employeer_home(request):
    company_name = request.user.company
    search_query = request.GET.get('search')
    job_listings = Job.objects.filter(company_name=company_name)
    
    if search_query:
        job_listings = job_listings.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)|
            Q(location__icontains=search_query)
        )

    job_listings = job_listings.order_by('-id')
    
    return render(request, 'employeer/employeer_home.html', {'job_listings': job_listings})
def job_application(request):
    application=JobApplication.objects.all()
    return render(request, 'employeer/job_application.html', {'application': application})
def update_status(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['ACCEPTED', 'REJECTED']:
            old_status = application.status
            application.status = new_status
            application.save()
            
            # Send email to the job seeker
            subject = f"Application Status Update for Job: {application.job.title}"
            job_seeker_email = application.email
            job_seeker_name = application.full_name
            email_template = 'employeer/job_seeker_status_notification.html'
            email_context = {
                'job_title': application.job.title,
                'new_status': new_status,
                'old_status': old_status,
                'job_seeker_name': job_seeker_name,
            }
            if new_status == 'ACCEPTED':
                email_context['message'] = "Congratulations! Your application has been accepted for the position."
            elif new_status == 'REJECTED':
                email_context['message'] = "We regret to inform you that your application has been rejected for the position."
            
            try:
                send_mail(subject, render_to_string(email_template, email_context), None, [job_seeker_email], fail_silently=False)
            except Exception as e:
                return HttpResponseServerError(f'An error occurred while sending email notification: {e}')
    
    return redirect('employeer:job_application')
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employeer:employeer_home')
    else:
        form = JobForm(instance=job)
    return render(request, 'employeer/edit_job.html', {'form': form})

def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        job.delete()
        return redirect('employeer:employeer_home')
    return render(request, 'employeer/delete_job_confirm.html', {'job': job})