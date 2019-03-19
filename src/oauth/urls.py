from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'oauth'

urlpatterns = [

    path('home/', views.home, name='home'),
    path('Farmer_Signup/',views.FarmerRegisterView,name='Farmer_Signup'),
    path('index/',views.index),

]
