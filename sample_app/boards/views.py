# Create your views here.
from toolkit.views import CCECreateView, reverse, CCEDeleteView, \
    CCEUpdateView
from toolkit.views import CCESearchView

from boards.forms import BoardSimpleSearch, BoardAdvancedSearchForm, BoardForm
from boards.models import Board

from toolkit.views import CCETemplateView


class DashboardView(CCETemplateView):
    sidebar_group = ['dashboard', ]
    template_name = 'base.html'

    def get_page_title(self):
        return "Welcome Back %s" % self.request.user.get_full_name()


class BoardListView(CCESearchView):
    model = Board
    page_title = 'Browse Boards'
    search_form_class = BoardSimpleSearch
    advanced_search_form_class = BoardAdvancedSearchForm
    sidebar_group = ['boards']
    columns = [
        ('Name', 'name'),
        ('Description', 'description'),
        ('Created at', 'created_at'),
        ('Created by', 'created_by'),
    ]
    paginate_by = 5
    show_context_menu = True

    def render_buttons(self, user, obj, *args, **kwargs):
        buttons = super(BoardListView, self).render_buttons(user, obj,
                                                            *args, **kwargs)
        buttons.append(

            self.render_button(btn_class='btn-info',
                               button_text='View',
                               icon_classes='glyphicon glyphicon-info-sign',
                               url=obj.get_absolute_url(),)
        )
        return buttons


class BoardCreateView(CCECreateView):
    model = Board
    form_class = BoardForm
    page_title = "Create a New Board!"
    sidebar_group = ['boards', ]
    success_message = "Board Created Successfully"


class BoardUpdateView(CCEUpdateView):
    model = Board
    page_title = 'Edit Board'
    sidebar_group = ['boards', ]
    form_class = BoardForm
    success_message = "Board Edited Successfully"


class BoardDeleteView(CCEDeleteView):
    model = Board
    page_title = 'Delete Board'
    success_message = "Board Deleted Successfully"
    sidebar_group = ['boards', ]

    def get_success_url(self):
        return reverse('browse_boards')
