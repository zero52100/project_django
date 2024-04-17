from django.urls import path
from . import views

app_name = 'job_seeker'

urlpatterns = [
    path('profile/', views.job_seeker_profile, name='profile'),
    path('apply_job/<int:job_id>', views.apply_job, name='apply_job'), 
    path('job_detail/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job_applied/', views.job_applied, name='job_applied'), 


]
