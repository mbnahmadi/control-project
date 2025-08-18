from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import LoginForm
from django.contrib.auth import logout
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "usersapp/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")  # بعد از لاگین کجا بره


def LogoutView(request):
    logout(request)
    return redirect("login")