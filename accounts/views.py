from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

class SignupView(auth_views.SignupView):
    template_name = "accounts/signup.html"
    success_url = "/"

class ProfileView(auth_views.ProfileView):
    template_name = "accounts/profile.html"
    success_url = "/"

class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    success_url = "/"