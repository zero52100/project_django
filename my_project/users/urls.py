from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('home1/', views.home1, name='home1'),
    path('complaint/', views.complaint, name='complaint'),
     path('view_complaint/', views.view_complaint, name='view_complaint'),
    
    
    
    
]