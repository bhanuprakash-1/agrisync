from django.views.generic import ListView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Topic, Answer
from .forms import TopicForm

class IndexView(LoginRequiredMixin,ListView):
    template_name = 'forum/index.html'
    context_object_name = 'topic_list'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context=super(IndexView,self).get_context_data(**kwargs)
        context['range']=range(context["paginator"].num_pages)
        return context

    def get_queryset(self):
        if self.request.GET.get('q'):
            query=self.request.GET.get('q')
            return Topic.objects.search(query)
        else:
            return Topic.objects.all()

class TopicCreateView(LoginRequiredMixin,CreateView):
    form_class = TopicForm
    template_name = 'forum/topic_forum.html'
    def form_invalid(self, form):
        form.instance.author=self.request.user.userprofile
        return super(TopicCreateView,self).form_valid(form)