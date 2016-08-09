"""sample_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

from boards.views import BoardListView, BoardCreateView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^board/', include("boards.urls")),
    url(r'^plank/', include("planks.urls")),
    url(r'^splinter/', include("splinters.urls")),
    url(r'^profiles/', include("profiles.urls")),

    url(r'^$', BoardListView.as_view(), name='home', ),

    url(r'^accounts/login/', 'django.contrib.auth.views.login', name="login", ),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout', name="logout", ),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
