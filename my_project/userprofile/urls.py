from django.urls import path, include

from .views import dashboard, view_application, view_dashboard_job,edit_profile,delete_user,admin_dashboard
from . import views

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('job/<int:job_id>/', view_dashboard_job, name='view_dashboard_job'),
    path('application/<int:application_id>/', view_application, name='view_application'),
    path('edit-profile/', edit_profile, name='edit_profile'),
     path('resumes/<path:resume_filename>/', views.serve_resume, name='serve_resume'),
     path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
     path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
     
    
    
]
