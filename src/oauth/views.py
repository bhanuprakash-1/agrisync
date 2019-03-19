from django.shortcuts import render, get_object_or_404 , redirect
from django.http import HttpResponse , HttpResponseRedirect
from .forms import FarmerRegisterForm,ExpertRegistrationForm
from .models import Farmer, Expert
from django.contrib.auth import authenticate , login
from django.urls import reverse
def home(request):
    return render(request,'oauth/home_oauth.html')


def index(request):
    return render(request,'oauth/index.html', {'user': None})


def createFarmerprofile(user=None, **kwargs):
    userprofile= Farmer.objects.create(user=user,
                                       full_name=kwargs['full_name'],
                                       phone=kwargs['phone'],
                                       dob=kwargs['dob'],
                                       aadhar=kwargs['aadhar'],
                                       img_file=kwargs['img_file'],
                                       land_area=kwargs['land_area'],
                                       state=kwargs['state'],
                                       district=kwargs['district'],
                                       income=kwargs['income'],
                                       major_crop=kwargs['major_crop'],


                                      )

    userprofile.save()

def FarmerRegisterView(request):
    if request.method == 'POST':
        form = FarmerRegisterForm(request.POST)

        if form.is_valid():
            user= form.save()
            username= form.cleaned_data['username']
            password= form.cleaned_data['password1']
            createFarmerprofile(user, **form.cleaned_data)
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('oauth:home'),{'user': user})

    else:
        form = FarmerRegisterForm()

    return render(request, 'oauth/Farmer_Signup.html',{'form': form})

