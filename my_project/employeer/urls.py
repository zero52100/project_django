from django.urls import path
from . import views

app_name = 'employeer'

urlpatterns = [
    path('employeer_profile/', views.employeer_profile, name='employeer_profile'),
    path('add_job/', views.add_job, name='add_job'),
    path('employeer_home/', views.employeer_home, name='employeer_home'),
    path('job_application/', views.job_application, name='job_application'),
    path('update_status/<int:application_id>/', views.update_status, name='update_status'),
    path('edit_job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    
]
