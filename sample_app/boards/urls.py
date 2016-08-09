from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from boards.views import BoardUpdateView, BoardDeleteView, BoardCreateView
from planks.views import PlankListView

urlpatterns = [
    url(r'^create_board/', login_required(BoardCreateView.as_view()), name='add_board', ),
    url(r'^(?P<pk>\d+)/', include([
        url(r'^$', PlankListView.as_view(), name='view_board'),
        url(r'^edit/$', login_required(BoardUpdateView.as_view()), name='edit_board'),
        url(r'^delete/$', login_required(BoardDeleteView.as_view()), name='delete_board'),
    ])),
]