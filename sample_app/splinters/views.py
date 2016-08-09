from django.contrib.auth.models import User
from django.shortcuts import render
from toolkit.views import CCESearchView, CCEDetailView, reverse, CCECreateView, CCEDeleteView, CCEUpdateView, \
    ReportDownloadSearchView

from planks.models import Plank
from splinters.forms import SplinterSimpleSearch, SplinterAdvancedSearchForm, SplinterForm
from splinters.models import Splinter


class SplinterListView(ReportDownloadSearchView):
    model = Splinter
    search_form_class = SplinterSimpleSearch
    advanced_search_form_class = SplinterAdvancedSearchForm
    sidebar_group = ['Splinter']
    columns = [
        ('Owner', 'owner'),
        ('Comment', 'comment'),
    ]
    show_context_menu = True

    def get_context_data(self, **kwargs):
        return super(SplinterListView, self).get_context_data(**kwargs)

    def get_page_title(self):
        plank = self.get_object()
        return plank.title

    def get_object(self):
        return Plank.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self):
        return Splinter.objects.filter(plank__pk=self.kwargs['pk'])

    def context_menu_items(self):
        items = super(SplinterListView, self).context_menu_items()
        items.append(
            (
                "Add Splinter",
                reverse('add_splinter', kwargs={'pk': self.kwargs['pk']}),
                "glyphicon glyphicon-plus",
                "Splinter",
            )
        ),
        items.append(
            (
                "Back To Plank",
                reverse('view_board', kwargs={'pk': self.get_object().board.pk}),
                "glyphicon glyphicon-share-alt",
                "Splinter",
            )
        ),
        return items

    def get_reports(self):
        return {
            'boards_report': {'name': 'Splinter Reports (xlsx)', 'method': 'splinter_creation_report'},
        }


class SplinterDetailView(CCEDetailView):
    model = Splinter
    page_title = "Splinter Details"
    sidebar_group = ['Splinter']
    detail_fields = [
        ('Owner', 'owner'),
        ('Comment', 'comment'),
    ]
    show_context_menu = True

    def context_menu_items(self):
        items = super(SplinterDetailView, self).context_menu_items()
        items.append(
            (
                "Back To Splinters",
                reverse('view_plank', kwargs={'pk': self.kwargs['pk']}),
                "glyphicon glyphicon-share-alt",
                "Splinter"
            )
        )
        return items


class SplinterCreateView(CCECreateView):
    model = Splinter
    sidebar_group = ['Splinter']
    page_title = 'Create Splinter'
    form_class = SplinterForm
    success_message = "Splinter Created Successfully"

    def get_success_url(self):
        return reverse('view_plank', kwargs={'pk': self.object.plank_id})

    def get_initial(self):
        return {'owner': User.objects.get(username=self.request.user),
                'plank': Plank.objects.get(pk=self.kwargs['pk'])}


class SplinterDeleteView(CCEDeleteView):
    model = Splinter
    sidebar_group = ['Splinter']
    page_title = "Delete Splinter"
    success_message = "Splinter Deleted Successfully"

    def get_success_url(self):
        return reverse('view_plank', kwargs={'pk': self.object.plank_id})


class SplinterUpdateView(CCEUpdateView):
    model = Splinter
    page_title = 'Edit Splinter'
    sidebar_group = ['Splinter']
    form_class = SplinterForm
    success_message = "Splinter Edited Successfully"

    def get_success_url(self):
        return reverse('view_plank', kwargs={'pk': self.object.plank_id})
