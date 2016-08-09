from django.contrib.auth.models import User
from toolkit.views import CCESearchView, CCECreateView, reverse, CCEDeleteView, CCEUpdateView, ReportDownloadSearchView

from boards.models import Board
from planks.forms import PlankSimpleSearch, PlankAdvancedSearchForm, PlankForm
from planks.models import Plank


class PlankListView(ReportDownloadSearchView):
    model = Plank
    page_title = "Test"
    search_form_class = PlankSimpleSearch
    advanced_search_form_class = PlankAdvancedSearchForm
    sidebar_group = ['Planks', ]
    columns = [
        ('Image', lambda x: "<img src='%s'>" % x.image.url),
        ('Title', 'title'),
        ('Created', 'created'),
        ('Owner', 'owner'),
    ]
    show_context_menu = True

    def get_context_data(self, **kwargs):
        return super(PlankListView, self).get_context_data(**kwargs)

    def get_page_title(self):
        board = Board.objects.get(pk=self.kwargs['pk'])
        return board.name

    def context_menu_items(self):
        items = super(PlankListView, self).context_menu_items()
        items.append(
            (
                "Add Plank",
                reverse('add_plank', kwargs={'pk': self.kwargs['pk']}),
                "glyphicon glyphicon-plus",
                "Plank",
            )
        ),
        items.append(
            (
                "Back To Boards",
                reverse('home'),
                "glyphicon glyphicon-share-alt",
                "Plank",
            )
        ),
        return items

    def get_queryset(self):
        return Plank.objects.filter(board=Board.objects.get(pk=self.kwargs['pk']))

    def get_reports(self):
        return {
            'boards_report': {'name': 'Plank Reports (xlsx)', 'method': 'plank_creation_report'},
        }


class PlankCreateView(CCECreateView):
    model = Plank
    sidebar_group = ['Planks']
    page_title = 'Create Plank'
    form_class = PlankForm
    success_message = "Plank Created Successfully"

    def get_success_url(self):
        return reverse('view_board', kwargs={'pk': self.object.board_id})

    def get_initial(self):
        return {'board': Board.objects.get(pk=self.kwargs['pk']),
                'owner': User.objects.get(username=self.request.user)}


class PlankDeleteView(CCEDeleteView):
    model = Plank
    sidebar_group = ['Plank']
    page_title = "Delete Plank"
    success_message = "Plank Deleted Successfully"

    def get_success_url(self):
        return reverse('view_board', kwargs={'pk': self.object.board_id})


class PlankUpdateView(CCEUpdateView):
    model = Plank
    page_title = 'Edit Board'
    sidebar_group = ['Plank']
    form_class = PlankForm
    success_message = "Plank Edited Successfully"

    def get_success_url(self):
        return reverse('view_board', kwargs={'pk': self.object.board_id})
