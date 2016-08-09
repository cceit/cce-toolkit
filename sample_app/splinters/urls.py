from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from splinters.views import SplinterCreateView, SplinterDetailView, SplinterUpdateView, SplinterDeleteView

urlpatterns = [
    # url(r'^create_splinter/', SplinterCreateView.as_view(), name='add_splinter'),
        url(r'^(?P<pk>\d+)/', include([
            url(r'^$', SplinterDetailView.as_view(), name='view_splinter'),
            url(r'^create_splinter/', login_required(SplinterCreateView.as_view()), name='add_splinter'),
            url(r'^edit/$', login_required(SplinterUpdateView.as_view()), name='edit_splinter'),
            url(r'^delete/$', login_required(SplinterDeleteView.as_view()), name='delete_splinter'),
        ])),
]