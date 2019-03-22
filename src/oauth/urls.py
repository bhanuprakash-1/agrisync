from django.urls import path
from . import views

app_name = 'oauth'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('Farmer_Signup/', views.FarmerRegisterView, name='Farmer_Signup'),
    path('Expert_Signup/', views.ExpertRegisterView, name='Expert_Signup'),
    path('Login/', views.LoginView, name='Login'),
    path('Logout/', views.LogoutView, name='Logout'),
]
