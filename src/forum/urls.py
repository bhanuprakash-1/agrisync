from django.conf.urls import url
from .views import IndexView,TopicCreateView


app_name = 'forum'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^topic/add/$', TopicCreateView.as_view(), name='add_topic'),
]
