from django.views import generic


class HomePage(generic.TemplateView):
    """
    Simple template view for rendering the home page of website.
    """
    template_name = "main/home.html"


class AboutPage(generic.TemplateView):
    """
    Simple template view for rendering the about page of website.
    """
    template_name = "main/about.html"
