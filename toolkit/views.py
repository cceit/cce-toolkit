from django.core.exceptions import FieldError
from django.db import ProgrammingError
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, TemplateView, FormView
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, ModelFormSetView

from toolkit.forms import ReportSelector
from toolkit.utils import hasfield
from .mixins.views import *


class CCECreateView(ViewMetaMixin, SuccessMessageMixin, ClassPermissionsMixin, CreateContextMenuMixin, CreateView):
    """
    This view includes all the mixins required in all CreateViews.
    """
    template_name = 'form.html'
    permissions = {'get': ['can_create'],
                   'post': ['can_create'], }


class CCEListView(ViewMetaMixin, ClassPermissionsMixin, AbstractedListMixin, ListContextMenuMixin, ListView):
    """
    This view includes all the mixins required in all ListViews.
    """
    permissions = {'get': ['can_view_list'],
                   'post': ['can_view_list'], }


class CCEUpdateView(ViewMetaMixin, SuccessMessageMixin, ObjectPermissionsMixin, UpdateContextMenuMixin, UpdateView):
    """
    This view includes all the mixins required in all UpdateViews.
    """
    template_name = 'form.html'
    permissions = {'get': ['can_update'],
                   'post': ['can_update'], }


class CCEDetailView(ViewMetaMixin, ObjectPermissionsMixin, AbstractedDetailMixin, DetailContextMenuMixin, DetailView):
    """
    This view includes all the mixins required in all DetailViews.
    """
    permissions = {'get': ['can_view'],
                   'post': ['can_view'], }


class CCEDeleteView(ViewMetaMixin, SuccessMessageMixin, ObjectPermissionsMixin, AbstractedDeleteMixin, DeleteView):
    """
    This view includes all the mixins required in all DeleteViews.
    """
    permissions = {'get': ['can_delete'],
                   'post': ['can_delete'],
                   'delete': ['can_delete'], }


class CCECreateWithInlinesView(ViewMetaMixin, SuccessMessageMixin, ClassPermissionsMixin, CreateContextMenuMixin, CreateWithInlinesView):
    """
    This view includes all the mixins required in all CreateWithInlinesViews.
    """
    permissions = {'get': ['can_create'],
                   'post': ['can_create'], }


class CCEUpdateWithInlinesView(ViewMetaMixin, SuccessMessageMixin, ObjectPermissionsMixin, UpdateContextMenuMixin, UpdateWithInlinesView):
    """
    This view includes all the mixins required in all UpdateWithInlinesViews.
    """
    permissions = {'get': ['can_update'],
                   'post': ['can_update'], }


class CCEModelFormSetView(ViewMetaMixin, SuccessMessageMixin, ClassPermissionsMixin, ModelFormSetView):
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
                qs.order_by(order_by)[0]  # used to force the query to be called to ensure that ordering string is valid
            except (ProgrammingError, FieldError):
                pass
            else:
                return qs.order_by(order_by)
        return qs

    def get_context_data(self, **kwargs):
        context = super(CCESearchView, self).get_context_data(**kwargs)
        context['search_form'] = self.get_search_form()
        if self.advanced_search_form_class:
            context['advanced_search_form'] = self.get_advanced_search_form_class()
        return context


class ReportSearchView_needswork(CCESearchView):
    """Variant of SearchView for displaying a report of the search results.

    base_search.html was designed for use with this view.

    The following attributes must be defined on inheriting classes:
        - model or queryset (per BaseListView)
        - search_form_class (per SearchView)
        - report_function: a function that will be applied to each object in
            object_list to generate a tabular report. See utils.generate_table.
            Note: due to Python's bound-method calling process, this function
            must either be fully defined on this class, or wrapped with
            'staticmethod' if it is assigned from an external definition (e.g.,
            `report_function = staticmethod(payment_contract_report)`), to
            avoid passing it a reference to 'self' as its first argument.
        - report_download_url (optional): the URL at which to download a report
            of the data displayed on the page. This URL should expect the same
            GET query string as this view. This attribute is simply passed to
            the template as context data.
    """
    report_function = None
    report_download_url = None

    def get_url(self, obj):
        """Return a URL for the given object, to link to from the report.

        This method may be overridden in inheriting classes to make the first
        column of the displayed report into a hyperlink. The link may be to the
        object's detail view page, a related page, or really anywhere.

        Args:
            obj: an instance of the ReportView's model.
        Returns:
            The URL to link to from the object's row of the report, or None.
        """
        pass

    def get_context_data(self, **kwargs):
        _object_list = kwargs.get('object_list')
        # list-ify the report rows, for compatibility with templates (?!?).
        report = (list(row) for row in self.report_function(_object_list))
        # The first element of the report is the table headers.
        table_headers = next(report)
        # Package up the rest along with links.

        class ListWrapper(list):
            """Wrapper around the built-in list that allows specifying arbitrary
            attributes via kwargs passed to __init__.
            """

            def __init__(self, iterable=None, **kwargs):
                super(ListWrapper, self).__init__(iterable)
                for kwarg, value in kwargs.items():
                    setattr(self, kwarg, value)

        object_list = [
            ListWrapper(report_row, link=self.get_url(obj))
            for report_row, obj
            in zip(report, _object_list)
            ]
        return super(ReportSearchView_needswork, self).get_context_data(
            table_headers=table_headers,
            report_rows=object_list,
            report_download_url=self.report_download_url,
            **kwargs
        )


class ReportDownloadView(object):
    report_selector_form_class = ReportSelector

    def get_reports(self):
        raise ImproperlyConfigured("define reports user get_reports")

    def get_report_selector_form(self):
        return self.report_selector_form_class(self.request.GET or None, reports_list=self.get_reports())

    def get_context_data(self, **kwargs):
        context = super(ReportDownloadView, self).get_context_data(**kwargs)
        context.update({
            'report_selector_form': self.get_report_selector_form(),
        })
        return context


class ReportDownloadSearchView(ReportDownloadView, CCESearchView):
    """Variant of SearchView that downloads the search results as an xls file.

    Raises Http404 if the GET parameters do not form a valid search query.
    If no query string is specified, gives a report of all objects returned
    by get_queryset.

    The following fields must be defined on inheriting classes:
        - model or queryset (per BaseListView)
        - search_form_class (per SearchView)
        - report_function (see ReportView)

    The following fields have default values that should probably be overridden:
        - filename
        - sheet_name


    return {'report_slug': {'name': ''
                            'report_function': ''
                            'model': ''}}

    """

    def get(self, request, *args, **kwargs):
        self.search_form = self.search_form_class(request.GET)
        report_selector = self.get_report_selector_form()
        reports = self.get_reports()
        selected_report = request.GET.get('get_reports')
        if self.search_form.is_valid() and selected_report in reports:
            report = reports[selected_report]
            model = report['model'] if 'model' in report else self.model
            return getattr(model.reports, str('%s' % report['method']))(qs=self.get_queryset(), form=self.search_form)
        return super(ReportDownloadSearchView, self).get(request, *args, **kwargs)


class ReportDownloadDetailView(ReportDownloadView, CCEDetailView):
    """

    """

    def get(self, request, *args, **kwargs):
        reports = self.get_reports()
        selected_report = request.GET.get('get_reports')
        if selected_report in reports:
            report = reports[selected_report]
            model = report['model'] if 'model' in report else self.model
            return getattr(model.reports, str('%s' % report['method']))(obj=self.get_object())
        return super(ReportDownloadDetailView, self).get(request, *args, **kwargs)
