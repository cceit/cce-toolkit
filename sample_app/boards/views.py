# Create your views here.
from toolkit.views import CCECreateView, reverse, CCEDeleteView, CCEUpdateView, ReportDownloadSearchView

from boards.forms import BoardSimpleSearch, BoardAdvancedSearchForm, BoardForm
from boards.models import Board


class BoardListView(ReportDownloadSearchView):
    model = Board
    search_form_class = BoardSimpleSearch
    advanced_search_form_class = BoardAdvancedSearchForm
    sidebar_group = ['home']
    columns = [
        ('Image', lambda x: "<img src='%s'>" % x.image.url),
        ('Name', 'name'),
        ('Description', 'description'),
        ('Created', 'created'),
    ]
    show_context_menu = True

    def get_queryset(self):
        return Board.objects.all()

    def get_context_data(self, **kwargs):
        return super(BoardListView, self).get_context_data(**kwargs)

    def get_page_title(self):
        if self.request.user.is_authenticated():
            return "Welcome Back %s" % self.request.user.first_name
        else:
            return "Welcome to DaBoard!"

    def context_menu_items(self):
        return super(BoardListView, self).context_menu_items()

    def get_reports(self):
        return {
            'boards_report': {'name': 'Board Reports (xlsx)', 'method': 'board_creation_report'},
        }


class BoardCreateView(CCECreateView):
    model = Board
    form_class = BoardForm
    page_title = "Create a New Board!"
    sidebar_group = ['management', ]
    success_message = "Board Created Successfully"

    def get_success_url(self):
        return reverse('home')


class BoardDeleteView(CCEDeleteView):
    model = Board
    page_title = 'Delete Board'
    success_message = "Board Deleted Successfully"
    sidebar_group = ['management', ]

    def get_success_url(self):
        return reverse('home')


class BoardUpdateView(CCEUpdateView):
    model = Board
    page_title = 'Edit Board'
    sidebar_group = ['management', ]
    form_class = BoardForm
    success_message = "Board Edited Successfully"

    def get_success_url(self):
        return reverse('home')
