from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic

from webpush import send_user_notification

from core.mixins import ProfileRequiredMixin
from accounts.models import User

from .utils import find_users


class IndexPage(ProfileRequiredMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = 'discovery/index.html'


def search(request):
    query = request.GET.get("query", "")
    user_score = find_users(query)
    print(user_score)
    for us in user_score:
        if us == request.user.id:
            continue
        user = User.objects.get(pk=us)
        print(user)
        payload = {'head': 'New Loog', 'body': 'Google!', 'url': 'https://google.com', 'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/How_to_use_icon.svg/1200px-How_to_use_icon.svg.png'}
        # TODO: Add this to celery
        send_user_notification(user, payload, 1000)
        print("Sent notif to ", user)
    return HttpResponse("OK")
