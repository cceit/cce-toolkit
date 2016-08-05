from django.shortcuts import render

# Create your views here.
from toolkit.views import CCESearchView, CCEDetailView

from boards.forms import BoardSimpleSearch, BoardAdvancedSearchForm
from boards.models import Board


class BoardListView(CCESearchView):
    model = Board
    search_form_class = BoardSimpleSearch
    advanced_search_form_class = BoardAdvancedSearchForm
    template_name = 'home.html'
    sidebar_group = ['home']

    def get_context_data(self, **kwargs):
        return super(BoardListView, self).get_context_data(**kwargs)

    def get_page_title(self):
        if self.request.user.is_authenticated():
            return "Welcome Back %s" % self.request.user.first_name
        else:
            return "Welcome to DaBoard!"
