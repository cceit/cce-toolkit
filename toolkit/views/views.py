from django.core.exceptions import FieldError
from django.db import ProgrammingError
from django.views.generic import CreateView, ListView, UpdateView, \
    DetailView, DeleteView, TemplateView, FormView
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, \
    ModelFormSetView

from toolkit.forms import ReportSelector
from .mixins import *


class CCECreateView(ViewMetaMixin, SuccessMessageMixin, ClassPermissionsMixin,
                    CreateContextMenuMixin, CreateView):
    """
    This view includes all the mixins required in all CreateViews.



    Usage:
        .. code-block:: python
            :linenos:

            class PollCreateView(CCECreateView):
                model = Poll
                form_class = PollCreateForm
                page_title = "Create a poll"
                sidebar_group = ['polls', ]
                success_message = "Poll added successfully."

    Advanced Usage:
        .. code-block:: python
            :linenos:

            class PollCreateView(CCECreateView):
                model = Poll
                form_class = PollCreateForm
                page_title = "Create a poll"
                sidebar_group = ['polls', ]
                success_message = "Poll added successfully."

    """
    template_name = 'form.html'
    permissions = {'get': ['can_create'],
                   'post': ['can_create'], }


class CCEListView(ViewMetaMixin, ClassPermissionsMixin, AbstractedListMixin,
                  ListContextMenuMixin, ListView):
    """
    This view includes all the mixins required in all ListViews.
    """
    permissions = {'get': ['can_view_list'],
                   'post': ['can_view_list'], }


class CCEUpdateView(ViewMetaMixin, SuccessMessageMixin,
                    ObjectPermissionsMixin, UpdateContextMenuMixin,
                    UpdateView):
    """
    This view includes all the mixins required in all UpdateViews.
    """
    template_name = 'form.html'
    permissions = {'get': ['can_update'],
                   'post': ['can_update'], }


class CCEDetailView(ViewMetaMixin, ObjectPermissionsMixin,
                    AbstractedDetailMixin, DetailContextMenuMixin, DetailView):
    """
    This view includes all the mixins required in all DetailViews.
    """
    permissions = {'get': ['can_view'],
                   'post': ['can_view'], }


class CCEDeleteView(ViewMetaMixin, SuccessMessageMixin,
                    ObjectPermissionsMixin, AbstractedDeleteMixin, DeleteView):
    """
    This view includes all the mixins required in all DeleteViews.
    """
    permissions = {'get': ['can_delete'],
                   'post': ['can_delete'],
                   'delete': ['can_delete'], }


class CCECreateWithInlinesView(ViewMetaMixin, SuccessMessageMixin,
                               ClassPermissionsMixin, CreateContextMenuMixin,
                               CreateWithInlinesView):
    """
    This view includes all the mixins required in all CreateWithInlinesViews.
    """
    permissions = {'get': ['can_create'],
                   'post': ['can_create'], }


class CCEUpdateWithInlinesView(ViewMetaMixin, SuccessMessageMixin,
                               ObjectPermissionsMixin, UpdateContextMenuMixin,
                               UpdateWithInlinesView):
    """
    This view includes all the mixins required in all UpdateWithInlinesViews.
    """
    permissions = {'get': ['can_update'],
                   'post': ['can_update'], }


class CCEModelFormSetView(ViewMetaMixin, SuccessMessageMixin,
                          ClassPermissionsMixin, ModelFormSetView):
    """
    This view includes all the mixins required in all ModelFormSetViews.
    """
    permissions = {
        'get': ['can_create', 'can_update'],
        'post': ['can_create', 'can_update'],
    }
    add_button_title = ''

    def get_add_button_title(self):
        if not self.add_button_title:
            raise ImproperlyConfigured("add_button_title is not set")
        return self.add_button_title

    def get_context_data(self, **kwargs):
        context = super(CCEModelFormSetView, self).get_context_data(**kwargs)
        context['add_button_title'] = self.get_add_button_title()
        return context


class CCETemplateView(ViewMetaMixin, TemplateView):
    """
    This view includes all the mixins required in all TemplateViews.
    """
    pass


class CCEFormView(ViewMetaMixin, FormView):
    """
    This view includes the mixins required for all FormViews.
    """
    pass


class CCESearchView(CCEListView):
    """ListView variant that filters the queryset on search parameters.

    The field 'search_form_class' must be defined as a subclass of SearchForm
    in inheriting classes.

    The field 'allow_empty' (inherited from MultipleObjectMixin) is ignored,
    since this view must allow an empty object_list.
    """
    search_form_class = None
    advanced_search_form_class = None

    def get_search_form(self):
        return self.search_form_class(self.request.GET or None)

    def get_advanced_search_form_class(self):
        if self.advanced_search_form_class:
            return self.advanced_search_form_class(self.request.GET or None)
        return None

    def get_queryset(self):
        """Filters the default queryset based on self.search_form.search.

        Requires self.search_form to be set before this function is called,
        probably in self.get.

        If self.search_form is invalid, returns an empty list.
        """
        qs = super(CCESearchView, self).get_queryset()
        order_by = self.request.GET.get('order_by', None)
        search_form = self.get_search_form()
        if search_form.is_valid():
            qs = search_form.search(qs)
        advanced_search_form = self.get_advanced_search_form_class()
        if advanced_search_form and advanced_search_form.is_valid():
            qs = advanced_search_form.search(qs)

        if qs and order_by and hasfield(self.model, order_by.replace('-', '')):
            try:
                qs.order_by(order_by)[0]
                # used to force the query to be called to ensure that
                # ordering string is valid
            except (ProgrammingError, FieldError):
                pass
            else:
                return qs.order_by(order_by)
        return qs

    def get_context_data(self, **kwargs):
        context = super(CCESearchView, self).get_context_data(**kwargs)
        context['search_form'] = self.get_search_form()
        if self.advanced_search_form_class:
            context['advanced_search_form'] = \
                self.get_advanced_search_form_class()
        return context


class ReportDownloadView(object):
    report_selector_form_class = ReportSelector

    def get_reports(self):
        raise ImproperlyConfigured("define reports user get_reports")

    def get_report_selector_form(self):
        return self.report_selector_form_class(self.request.GET or None,
                                               reports_list=self.get_reports())

    def get_context_data(self, **kwargs):
        context = super(ReportDownloadView, self).get_context_data(**kwargs)
        context.update({
            'report_selector_form': self.get_report_selector_form(),
        })
        return context


class ReportDownloadSearchView(ReportDownloadView, CCESearchView):
    """
    Variant of SearchView that downloads the search results as an xls file.

    Raises Http404 if the GET parameters do not form a valid search query.
    If no query string is specified, gives a report of all objects returned
    by get_queryset.

    The following fields must be defined on inheriting classes:
     - model or queryset (per BaseListView)
     - search_form_class (per SearchView)
     - report_function (see ReportView)

    The following fields have default values that should probably be
     overridden:
     - filename
     - sheet_name
    """

    def get(self, request, *args, **kwargs):
        self.search_form = self.search_form_class(request.GET)
        report_selector = self.get_report_selector_form()
        reports = self.get_reports()
        selected_report = request.GET.get('get_reports')
        if self.search_form.is_valid() and selected_report in reports:
            report = reports[selected_report]
            model = report['model'] if 'model' in report else self.model
            return getattr(model.reports, str('%s' % report['method']))(
                qs=self.get_queryset(), form=self.search_form)
        return super(ReportDownloadSearchView, self).get(request, *args,
                                                         **kwargs)


class ReportDownloadDetailView(ReportDownloadView, CCEDetailView):
    """

    """

    def get(self, request, *args, **kwargs):
        reports = self.get_reports()
        selected_report = request.GET.get('get_reports')
        if selected_report in reports:
            report = reports[selected_report]
            model = report['model'] if 'model' in report else self.model
            return getattr(model.reports, str('%s' % report['method']))(
                obj=self.get_object())
        return super(ReportDownloadDetailView, self).get(request, *args,
                                                         **kwargs)
