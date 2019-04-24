from django.views.generic import ListView, CreateView, View, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Topic
from .forms import TopicForm, AnswerForm
from django.views.generic.detail import SingleObjectMixin


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'forum/index.html'
    context_object_name = 'topic_list'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['range'] = range(context["paginator"].num_pages)
        return context

    def get_queryset(self):
        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
            return Topic.objects.search(query)
        else:
            return Topic.objects.all()


class TopicDetailView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = TopicDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TopicAnswer.as_view()
        return view(request, *args, **kwargs)


class TopicDisplay(DetailView):
    model = Topic
    context_object_name = 'topic'
    template_name = 'forum/topic_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TopicDisplay, self).get_context_data(**kwargs)
        context['answer_list'] = self.object.answer_set.all()
        context['form'] = AnswerForm()
        return context


class TopicAnswer(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'forum/topic_detail.html'
    form_class = AnswerForm
    model = Topic

    def get_context_data(self, **kwargs):
        context = super(TopicAnswer, self).get_context_data(**kwargs)
        context['answer_list'] = self.object.answer_set.all()
        return context


class TopicCreateView(LoginRequiredMixin, CreateView):
    form_class = TopicForm
    template_name = 'forum/topic_forum.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(TopicCreateView, self).form_valid(form)
