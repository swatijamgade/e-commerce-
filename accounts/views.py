from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View

from .forms import SignUpForm, LoginForm, ProfileForm
from .models import Profile


@login_required
def dashboard(request):
    pass


# Create your views here.
class DashboardView(View):
    template_name = 'accounts/dashboard.html'

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        admin_context = {}
        user_context = {}
        if user.profile.role == 'ADMIN':
            messages.success(request, "Welcome to the dashboard")
            render(self.request, self.template_name, context=admin_context)
        else:
            messages.success(request, "Welcome to the dashboard")
            render(self.request, self.template_name, context=user_context)
        if True:
            messages.success(request, "Welcome to the dashboard")
        messages.error(request, "Error", extra_tags="alert alert-success")
        return render(self.request, self.template_name, {})


class SignUpView(View):
    form_class = SignUpForm
    template_name = 'registration/registration_done.html'
    initial_template = 'registration/register.html'

    def get(self, request):
        user_form = self.form_class()
        return render(request, self.initial_template, {'user_form': user_form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # create a new user object but avoid saving it yet
            new_user = form.save(commit=False)  # User object
            # set the chosen password
            password = form.cleaned_data.get('password1')
            new_user.set_password(password)
            # save the user object
            new_user.save()
            messages.success(request, "user registered")
            return render(request, self.template_name, context={'new_user': new_user})
        else:
            messages.error(request, "Form has error, please check")
            return render(request, self.initial_template)


class LoginView(View):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # view_url = reverse('accounts:logout')
                    return HttpResponseRedirect(reverse('accounts:dashboard'))
                else:
                    return HttpResponse('Disabled accounts')
            else:
                return HttpResponse('Invalid Login')
        else:
            form = LoginForm()
            return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """
    Logs out user from session
    """

    template_name = 'registration/logout.html'

    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return render(self.request, self.template_name)


class ProfileView(View):
    template_name = 'accounts/profile.html'

    @method_decorator(login_required)
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        return render(self.request, self.template_name, {'profile': profile})

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.mobile = form.cleaned_data.get('mobile')
            profile.save()
            return render(self.request, self.template_name, {'profile': profile})
        else:
            return render(self.request, self.template_name, {'profile': profile})


def add_address_view(request):
    pass

def update_address_view(request):
    pass

def update_profile_view(request):
    pass