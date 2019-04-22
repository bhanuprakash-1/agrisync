from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView as DefaultLoginView
from account.forms import FarmerForm, UserForm, ExpertForm
from account.models import FarmerAccount, ExpertAccount


class ProfileView(TemplateView):
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
            return url or '/admin'
        elif not hasattr(self.request.user, 'farmeraccount') or hasattr(self.request.user, 'expertaccount'):
            return reverse('forum:index')
        else:
            return '/'


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
        else:
            return super().get_success_url()


class AbstractCreateView(CreateView):
    request = None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.request = request
            return super(AbstractCreateView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse('account:register'))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.request = request
            return super(AbstractCreateView, self).post(request, *args, **kwargs)
        else:
            return redirect(reverse('account:register'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class FarmerRegisterView(AbstractCreateView):
    template_name = 'account/farmer_register.html'
    form_class = FarmerForm
    model = FarmerAccount


class ExpertRegisterView(AbstractCreateView):
    template_name = 'account/expert_register.html'
    form_class = ExpertForm
    model = ExpertAccount
