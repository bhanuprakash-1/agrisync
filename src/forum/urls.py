from django.conf.urls import url
from forum import views

app_name = 'forum'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^topic/add/$', views.TopicCreateView.as_view(), name='add_topic'),
    url(r'^topic/(?P<slug>[\w-]+)/$', views.TopicDetailView.as_view(), name='topic_detail'),
]
