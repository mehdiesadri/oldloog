from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from discovery.views import discover


class HomePage(generic.TemplateView):
    """
    Simple template view for rendering the home page of website.
    """
    template_name = "main/main.html"


class RegisterPage(SuccessMessageMixin, generic.CreateView):
    """
    Creates a new user based on built-in django user model.
    """
    template_name = "main/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('main:login')
    success_message = _("Your profile was created successfully")


class LoginPage(auth_views.LoginView):
    template_name = "main/login.html"


class LogoutView(auth_views.LogoutView):
    pass


def search(request):
    if request.method == "POST":
        username = request.user.username
        query = request.POST.get("query")

    return discover(request, username, query)
