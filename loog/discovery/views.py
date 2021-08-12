from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic

from core.mixins import ProfileRequiredMixin
from .utils import find_users


class IndexPage(ProfileRequiredMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = 'discovery/index.html'


def search(request):
    query = request.GET.get("query", "")
    user_score = find_users(query)
    print(user_score)
    return HttpResponse("OK")
