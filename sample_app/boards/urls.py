from django.conf.urls import url

from planks.views import PlankListView

urlpatterns = [
    url(r'^(?P<slug>[\w\-]+)$', PlankListView.as_view(), name='view_board', ),
]