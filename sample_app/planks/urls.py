from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from planks.views import PlankCreateView, PlankUpdateView, PlankDeleteView, PlankListView
from splinters.views import SplinterListView

urlpatterns = [
    url(r'^(?P<pk>\d+)/', include([
        url(r'^$', SplinterListView.as_view(), name='view_plank'),
        url(r'^create_plank/', login_required(PlankCreateView.as_view()), name='add_plank'),
        url(r'^edit/$', login_required(PlankUpdateView.as_view()), name='edit_plank'),
        url(r'^delete/$', login_required(PlankDeleteView.as_view()), name='delete_plank'),
    ])),
]