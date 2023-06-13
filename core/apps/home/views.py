from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.utils import timezone
from django.views import generic


class HomeView(generic.TemplateView):
    template_name = 'home/home.html'


class CustomLoginView(LoginView):
    username_field = 'email'
    template_name = 'home/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            self.request.user.last_login = timezone.now()
            return redirect('home:home')
        else:
            return super().form_valid(form)

