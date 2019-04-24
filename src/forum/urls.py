from django.conf.urls import url
from forum import views

app_name = 'forum'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^topic/add/$', views.TopicCreateView.as_view(), name='add_topic'),
    url(r'^(?P<slug>[\w-]+)/$', views.TopicDetailView.as_view(), name='detail'),
]
