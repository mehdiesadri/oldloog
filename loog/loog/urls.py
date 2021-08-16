"""loog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/discovery/", include("discovery.api.routers")),
    path("discovery/", include("discovery.urls", namespace="discovery")),
    path("chat/", include(("chat.urls", "chat"), namespace="chat")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path('accounts/oauth/', include('allauth.urls')),
    path("api/accounts/", include("accounts.api.routers")),
    path("", include("main.urls", namespace="main")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
