from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from core.mixins import ProfileRequiredMixin


class IndexPage(ProfileRequiredMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = 'discovery/index.html'


def discover(request, username, query):
    pass
