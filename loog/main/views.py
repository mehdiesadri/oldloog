from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import generic

from discovery.views import discover
from .tokens import registration_token


class HomePage(generic.TemplateView):
    """
    Simple template view for rendering the home page of website.
    """
    template_name = "main/main.html"


class LoginPage(auth_views.LoginView):
    """
    Session-based login.
    Note: It will redirect to homepage after a successful login.
    You can change this in settings --> LOGIN_REDIRECT_URL
    """
    template_name = "main/login.html"


class LogoutView(auth_views.LogoutView):
    """
    Session-based logout.
    Note: It will redirect to login page after a successful logout.
    You can change this in settings --> LOGOUT_REDIRECT_URL
    """
    pass


class RegisterView(generic.View):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and registration_token.check_token(user, token):
            # user.profile.email_confirmed = True
            # user.save()
            # login(request, user)
            return HttpResponse("Link is OK")
        else:
            # invalid link
            print(registration_token.check_token(user, token))
            return HttpResponse("Link is NOT OK")

def search(request):
    if request.method == "POST":
        username = request.user.username
        query = request.POST.get("query")

    return discover(request, username, query)
