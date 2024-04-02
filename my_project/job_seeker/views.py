from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.shortcuts import render, get_object_or_404
from employeer.models import Job
from .forms import JobApplicationForm
from .models import JobApplication
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseServerError
@login_required
def job_seeker_profile(request):
    
    job_seeker = request.user
    user_email = request.user.email
    user_type = request.user.userprofile.user_type
    
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
           
            job_seeker.email = form.cleaned_data['email']
            job_seeker.save()
            form.save()
            return redirect('job_seeker:profile')
    else:
        form = ProfileForm(instance=request.user.userprofile, initial={'email': user_email})

    
    return render(request, 'job_seeker/profile.html', {'job_seeker': job_seeker, 'user_email': user_email, 'user_type': user_type, 'form': form})
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    user = request.user
    user_has_applied = JobApplication.objects.filter(user=user, job=job).exists()
    context = {'job': job, 'user_has_applied': user_has_applied}
    return render(request, 'job_seeker/job_detail.html', context)

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    user_email = request.user.email
    job_seeker = request.user
    employeer = request.user
    user_email = request.user.email
    user_type = request.user.userprofile.user_type
    cover_letter = request.user.userprofile.cover_letter
    resume = request.user.userprofile.resume
    full_name = request.user.userprofile.full_name
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            application.username = request.user.username
            application.email = form.cleaned_data['email']
            application.full_name = request.user.userprofile.full_name
            application.UserProfile = request.user.userprofile
            
            if not form.cleaned_data['resume']:
                
                application.resume = resume
            
            application.save()
            employer_email = job.user_email
            subject_employeer = f"New Job Application for {job.title}"
            subject_job_seeker = f"Your Job Application Submmited for {job.title}"
            applicant_name = request.user.userprofile.full_name
            applicant_email = request.user.email
            job_status = job_seeker.jobapplication_set.filter(job=job).first().status
            email_template_employeer = 'job_seeker/employer_notification_email.html'
            email_template_job_seeker = 'job_seeker/job_seeker_notification_email.html'
            email_context_employer = {
                'job_title': job.title,
                'applicant_name': applicant_name,
                'applicant_email': applicant_email,
            }
            email_context_job_seeker = {
                'job_title': job.title,
                'applicant_name': applicant_name,
                'status':job_status
            }
            try:
                send_mail(subject_employeer, render_to_string(email_template_employeer, email_context_employer), user_email, [employer_email], fail_silently=False)
                send_mail(subject_job_seeker, render_to_string(email_template_job_seeker, email_context_job_seeker), user_email, [applicant_email], fail_silently=False)
            except BadHeaderError:
                return HttpResponseServerError('Invalid header found.')
            except Exception as e:
                return HttpResponseServerError(f'An error occurred: {e}')
            return redirect('home')
            
    else:
        
        initial_data = {'email': user_email, 'username': request.user.username, 'cover_letter': cover_letter, 'full_name': full_name}
        
        if resume:
            initial_data['resume'] = resume
        form = JobApplicationForm(initial=initial_data)
    
    return render(request, 'job_seeker/apply_job.html', {'form': form, 'job': job, 'user_email': user_email, 'job_seeker': job_seeker, 'user_type': user_type,'full_name':full_name})

def job_applied(request):
    user = request.user
    
    job_applied = JobApplication.objects.filter(user=user)
    return render(request, 'job_seeker/job_applied.html', {'job_applied': job_applied})