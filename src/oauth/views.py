from django.shortcuts import render, redirect
from .forms import FarmerRegisterForm, ExpertRegistrationForm
from .models import Farmer, Expert


def home(request):
    return render(request, 'oauth/home_oauth.html', )


def home(request, MAINTENANCE):
    return render(request, 'oauth/home_oauth.html', )


def createFarmerprofile(user=None, **kwargs):
    userprofile = Farmer.objects.create(user=user,
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
            user = form.save()
            createFarmerprofile(user, **form.cleaned_data)
            return redirect('/oauth/home/')

    else:
        form = FarmerRegisterForm()

    return render(request, 'oauth/Farmer_Signup.html', {'form': form})


def createExpertprofile(user=None, **kwargs):
    userprofile = Expert.objects.create(user=user,
                                        full_name=kwargs['full_name'],
                                        email_id=kwargs['email_id'],
                                        phone=kwargs['phone'],
                                        dob=kwargs['dob'],
                                        skills=kwargs['skills'],
                                        postal_add=kwargs['postal_add'],
                                        img_file=kwargs['img_file'],

                                        )
    userprofile.save()


def ExpertRegisterView(request):
    if request.method == 'POST':
        form = ExpertRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            createExpertprofile(user, **form.cleaned_data)
            return redirect('/oauth/home/')

    else:
        form = ExpertRegistrationForm()
    return render(request, 'oauth/Expert_Signup.html', {'form': form})
