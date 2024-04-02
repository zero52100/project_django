from django.urls import path
from . import views

app_name = 'admin1'  # Define app namespace

urlpatterns = [
    path('', views.admin1_home, name='admin1_home'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'), 
   
]
