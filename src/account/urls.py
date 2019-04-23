from django.conf.urls import url
from account.views import RegisterView, FarmerRegisterView, ProfileView, ExpertRegisterView

app_name = 'account'

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='profile'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^register/farmer/$', FarmerRegisterView.as_view(), name='farmer-register'),
    url(r'^register/expert/$', ExpertRegisterView.as_view(), name='expert-register'),
]
