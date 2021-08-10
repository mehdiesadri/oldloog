from django.views import generic

from discovery.views import discover


class HomePage(generic.TemplateView):
    """
    Simple template view for rendering the home page of website.
    """
    template_name = "main/main.html"


def search(request):
    if request.method == "POST":
        username = request.user.username
        query = request.POST.get("query")

    return discover(request, username, query)
