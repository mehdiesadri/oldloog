from django.views import generic

from core.mixins import ProfileRequiredMixin


class IndexPage(ProfileRequiredMixin, generic.TemplateView):
    template_name = 'discovery/index.html'
