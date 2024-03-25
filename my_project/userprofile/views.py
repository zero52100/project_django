from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from job.models import Job, Application
from .models import ConversationMessage
from notification.utilities import create_notification

from .models import Userprofile

from django.http import FileResponse
def admin_dashboard(request):
    # Add your view logic here
    return render(request, 'core/admin_dashboard.html')
def serve_resume(request, resume_filename):
    user_profile = get_object_or_404(Userprofile, resume=resume_filename)
    # Assuming 'resume' is the name of the FileField where resumes are stored
    resume_file = user_profile.resume

    return FileResponse(resume_file.open('rb'), content_type='application/pdf')  

@login_required
def dashboard(request):
    userprofile = request.user.userprofile
    
    # Check if the user is authorized to view the restricted dashboard
    if request.user.email == 'tewest2@gmail.com':
        # Gather statistics for all users
        total_employers = Userprofile.objects.filter(is_employer=True).count()
        total_employees = Userprofile.objects.filter(is_employer=False).count()
        total_jobs = Job.objects.all().count()
        all_users = User.objects.all()
        return render(request, 'userprofile/restricted_dashboard.html', {'total_employers': total_employers, 'total_employees': total_employees, 'total_jobs': total_jobs,'all_users': all_users})
    
    # Normal dashboard view for other users
    gender = request.user.profile.gender
    company_name = None
    designation = None

    if userprofile.is_employer:
        company_name = request.user.profile.company_name
        designation = request.user.profile.designation

    return render(request, 'userprofile/dashboard.html', {'userprofile': userprofile, 'company_name': company_name, 'designation': designation, 'gender': gender})

@login_required
def view_application(request, application_id):
    if request.user.userprofile.is_employer:
        application = get_object_or_404(Application, pk=application_id, job__created_by=request.user)
    else:
        application = get_object_or_404(Application, pk=application_id, created_by=request.user)
    
    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            conversationmessage = ConversationMessage.objects.create(application=application, content=content, created_by=request.user)

            create_notification(request, application.created_by, 'message', extra_id=application.id)

            return redirect('view_application', application_id=application_id)
    
    return render(request, 'userprofile/view_application.html', {'application': application})

@login_required
@login_required
@login_required
def edit_profile(request):
    userprofile = request.user.userprofile
    
    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter')
        if cover_letter:
            userprofile.cover_letter = cover_letter
        
        if userprofile.is_employer:
            company_name = request.POST.get('company_name')
            designation = request.POST.get('designation')
            if company_name:
                request.user.profile.company_name = company_name
            if designation:
                request.user.profile.designation = designation
        
        request.user.profile.save()  # Save changes to the UserProfile instance
        return redirect('dashboard')  # Redirect to the dashboard after saving
        
    return render(request, 'userprofile/edit_profile.html', {'userprofile': userprofile})
@login_required
def view_dashboard_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id, created_by=request.user)

    return render(request, 'userprofile/view_dashboard_job.html', {'job': job})
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('admin_dashboard')