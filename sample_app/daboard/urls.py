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

from tasks.views import TaskListView

urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + [
                    url(r'^admin/', include(admin.site.urls)),

                    url(r'^p/', include("tasks.urls")),
                    url(r'^profiles/', include("profiles.urls")),

                    url(r'^accounts/login/', 'django.contrib.auth.views.login',
                        name="login", ),
                    url(r'^accounts/logout/',
                        'django.contrib.auth.views.logout',
                        name="logout", ),

                    url(r'', include("boards.urls")),

              ]

