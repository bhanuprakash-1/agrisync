from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView as DefaultLoginView
from account.forms import FarmerForm, UserForm, ExpertForm
from account.models import FarmerAccount, ExpertAccount


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'
    user = None

    def get(self, request, *args, **kwargs):
        self.user = request.user
        return super(ProfileView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context


class LoginView(DefaultLoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        url = super().get_redirect_url()
        if self.request.user.is_staff:
            return url or reverse('admin:index')
        elif hasattr(self.request.user, 'farmeraccount') or hasattr(self.request.user, 'expertaccount'):
            return reverse('forum:index')
        else:
            return reverse('account:farmer-register')


class RegisterView(CreateView):
    template_name = 'account/register.html'
    form_class = UserForm
    model = User
    chosen_type = None

    def post(self, request, *args, **kwargs):
        self.chosen_type = request.POST.get('account_type', None)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        if self.chosen_type == 'FA':
            login(self.request, self.object)
            return reverse('account:farmer-register')
        elif self.chosen_type == 'EA':
            login(self.request, self.object)
            return reverse('account:expert-register')
        else:  # pragma: never happen
            return super().get_success_url()


class AbstractCreateView(LoginRequiredMixin, CreateView):
    request = None

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AbstractCreateView, self).form_valid(form)


class FarmerRegisterView(AbstractCreateView):
    template_name = 'account/farmer_register.html'
    form_class = FarmerForm
    model = FarmerAccount


class ExpertRegisterView(AbstractCreateView):
    template_name = 'account/expert_register.html'
    form_class = ExpertForm
    model = ExpertAccount
