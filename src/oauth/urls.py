from django.conf.urls import url
from oauth.views import home, FarmerRegisterView, ExpertRegisterView

app_name = 'oauth'

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^Farmer_Signup/$', FarmerRegisterView, name='Farmer_Signup'),
    url(r'^Expert_Signup/$', ExpertRegisterView, name='Expert_Signup'),
]
