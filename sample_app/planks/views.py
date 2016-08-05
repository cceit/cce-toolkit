from toolkit.views import CCESearchView

from boards.models import Board
from planks.forms import PlankSimpleSearch, PlankAdvancedSearchForm
from planks.models import Plank


class PlankListView(CCESearchView):
    model = Plank
    search_form_class = PlankSimpleSearch
    advanced_search_form_class = PlankAdvancedSearchForm
    sidebar_group = ['Board']

    def get_context_data(self, **kwargs):
        return super(PlankListView, self).get_context_data(**kwargs)

    def get_page_title(self):
        board = Board.objects.get(slug=self.kwargs['slug'])
        return board.name