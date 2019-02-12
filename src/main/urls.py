from django.conf.urls import url
from .views import HomeView


app_name = 'main'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='index')
]
