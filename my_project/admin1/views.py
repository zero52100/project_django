from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from users.models import UserProfile
from employeer.models import Job
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User

@staff_member_required
def admin1_home(request):
    total_job_seekers = UserProfile.objects.filter(user_type='job_seeker').count()
    total_employers = UserProfile.objects.filter(user_type='employer').count()
    total_jobs = Job.objects.count()
    job_seekers = UserProfile.objects.filter(user_type='job_seeker')
    employers = UserProfile.objects.filter(user_type='employer')

    context = {
        'total_job_seekers': total_job_seekers,
        'total_employers': total_employers,
        'total_jobs': total_jobs,
        'job_seekers': job_seekers,
        'employers': employers,
    }

    return render(request, 'admin1/admin1_home.html', context)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin1:admin1_home')
