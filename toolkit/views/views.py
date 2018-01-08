from django.core.exceptions import FieldError
from django.db import ProgrammingError
from django.views.generic import CreateView, ListView, UpdateView, \
    DetailView, DeleteView, TemplateView, FormView
from django.views.generic import RedirectView
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
                template_name = "polls/add.html"
                page_title = "Create a poll"
                sidebar_group = ['polls', ]
                success_message = "Poll added successfully."

                def context_menu_items(self):
                    items = super(PollListView, self).context_menu_items()
                    items.append(
                        # label, reversed url, icon class, sidebar_group
                        (
                            "Link to something else you want",
                            reverse('link_to_something_else'),
                            "glyphicon glyphicon-fire",
                            "something_else",
                        )
                    )
                    return items
    """
    template_name = 'form.html'
    permissions = {'get': ['can_create'],
                   'post': ['can_create'], }


class CCEListView(ViewMetaMixin, ClassPermissionsMixin, AbstractedListMixin,
                  ListContextMenuMixin, ListView):
    """
    This view includes all the mixins required in all ListViews.

    Usage:
        .. code-block:: python
            :linenos:

            class PollListView(CCEListView):
                model = Poll
                paginate_by = 10
                page_title = "Browse Polls"
                sidebar_group = ['polls', ]
                columns = [
                    ('Name', 'name'),
                    ('Active', 'active'),
                ]
                show_context_menu = True

    Advanced Usage:
        .. code-block:: python
            :linenos:

            class PollListView(CCEListView):
                model = Poll
                paginate_by = 10
                template_name = "polls/list.html"
                ordering = ['-created_at']
                page_title = "Browse Polls"
                sidebar_group = ['polls', ]
                # Column widths should add up to 12
                columns = [
                    ('Name', 'name', 4),
                    ('Active', 'active', 5),
                ]
                actions_column_width = 3
                show_context_menu = True
                show_add_button = True
                popover_rows = [
                    ('Description', 'description'),
                    ('Choices', lambda poll: some_function(poll)),
                ]

                def context_menu_items(self):
                    items = super(PollListView, self).context_menu_items()
                    items.append(
                        # label, reversed url, icon class, sidebar_group
                        (
                            "Edit All Polls at Once",
                            reverse('edit_all_polls'),
                            "glyphicon glyphicon-pencil",
                            "edit_all_polls",
                        )
                    )
                    return items

                def render_buttons(self, user, obj, **kwargs):
                    button_list = super(PollListView, self).render_buttons(user, obj, **kwargs)
                    button_list.extend([
                        self.render_button(
                            url_name='edit_poll_permissions',
                            pk=obj.pk,
                            icon_classes='fa fa-lock',
                        ),
                        self.render_button(
                            btn_class='warning',
                            label='Button text',
                            icon_classes='glyphicon glyphicon-fire',
                            url=reverse('some_url_name_no_pk_required'),
                            condensed=False,
                        ),
                    ])
                    return button_list
    """
    permissions = {'get': ['can_view_list'],
                   'post': ['can_view_list'], }

    def get_queryset(self):
        """
        Orders the queryset based on the order_by query param in the url
        """
        qs = super(CCEListView, self).get_queryset()
        order_by = self.request.GET.get('order_by', None)
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


class CCEUpdateView(ViewMetaMixin, SuccessMessageMixin,
                    ObjectPermissionsMixin, UpdateContextMenuMixin,
                    UpdateView):
    """
    This view includes all the mixins required in all UpdateViews.

    Usage:
        .. code-block:: python
            :linenos:

            class PollUpdateView(CCECreateView):
                model = Poll
                form_class = PollUpdateForm
                page_title = "Edit Poll"
                sidebar_group = ['polls', ]
                success_message = "Poll saved successfully."

    Advanced Usage:
        .. code-block:: python
            :linenos:

            class PollUpdateView(CCECreateView):
                model = Poll
                form_class = PollUpdateForm
                template_name = "polls/edit.html"
                page_title = "Edit Poll"
                sidebar_group = ['polls', ]
                success_message = "Poll saved successfully."

                def context_menu_items(self):
                    items = super(PollUpdateView, self).context_menu_items()
                    items.append(
                        # label, reversed url, icon class, sidebar_group
                        (
                            "Link to something else you want",
                            reverse('link_to_something_else'),
                            "glyphicon glyphicon-fire",
                            "something_else",
                        )
                    )
                    return items
    """
    template_name = 'form.html'
    permissions = {'get': ['can_update'],
                   'post': ['can_update'], }


class CCEDetailView(ViewMetaMixin, ObjectPermissionsMixin,
                    AbstractedDetailMixin, DetailContextMenuMixin, DetailView):
    """
    This view includes all the mixins required in all DetailViews.

    Usage:
        .. code-block:: python
            :linenos:

            class PollDetailView(CCEDetailView):
                model = Poll
                page_title = "Poll Details"
                sidebar_group = ['polls']
                detail_fields = [
                    ('Name', 'name'),
                    ('Active', 'active'),
                    ('Description', 'description'),
                    ('Choices', lambda poll: some_function(poll)),
                ]
                show_context_menu = True

    Advanced Usage:
        .. code-block:: python
            :linenos:

            class PollDetailView(CCEDetailView):
                model = Poll
                page_title = "Poll Details"
                sidebar_group = ['polls']
                detail_fields = [
                    ('Name', 'name'),
                    ('Active', 'active'),
                    ('Description', 'description'),
                    ('Choices', lambda poll: some_function(poll)),
                ]
                show_context_menu = True

                def context_menu_items(self):
                    items = super(PollDetailView, self).context_menu_items()
                    items.append(
                        # label, reversed url, icon class, sidebar_group
                        (
                            "Link to something else you want",
                            reverse('link_to_something_else'),
                            "glyphicon glyphicon-fire",
                            "something_else",
                        )
                    )
                    return items
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


class CCERedirectView(ClassPermissionsMixin, RedirectView):
    """
    This view includes all the mixins required in all RedirectViews.
    """
    permissions = {
        'get': ['can_view', ],
        'post': ['can_view', ],
    }


class CCEObjectRedirectView(ObjectPermissionsMixin, RedirectView):
    """
    This view includes all the mixins required in all RedirectViews.
    """
    permissions = {
        'get': ['can_view', ],
        'post': ['can_view', ],
    }

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

    Usage:
        .. code-block:: python
            :linenos:

            class PollListView(CCESearchView):
                model = Poll
                paginate_by = 10
                page_title = "Browse Polls"
                sidebar_group = ['polls', ]
                search_form_class = PollSimpleSearchForm
                advanced_search_form_class = PollAdvancedSearchForm
                columns = [
                    ('Name', 'name'),
                    ('Active', 'active'),
                ]
                show_context_menu = True

    Advanced Usage:
        .. code-block:: python
            :linenos:

            class PollListView(CCESearchView):
                model = Poll
                paginate_by = 10
                template_name = "polls/list.html"
                ordering = ['-created_at']
                page_title = "Browse Polls"
                sidebar_group = ['polls', ]
                search_form_class = PollSimpleSearchForm
                advanced_search_form_class = PollAdvancedSearchForm
                # Column widths should add up to 12
                columns = [
                    ('Name', 'name', 4),
                    ('Active', 'active', 5),
                ]
                actions_column_width = 3
                show_context_menu = True
                show_add_button = True
                popover_rows = [
                    ('Description', 'description'),
                    ('Choices', lambda poll: some_function(poll)),
                ]

                def context_menu_items(self):
                    items = super(PollListView, self).context_menu_items()
                    items.append(
                        # label, reversed url, icon class, sidebar_group
                        (
                            "Edit All Polls at Once",
                            reverse('edit_all_polls'),
                            "glyphicon glyphicon-pencil",
                            "edit_all_polls",
                        )
                    )
                    return items

                def render_buttons(self, user, obj, **kwargs):
                    button_list = super(PollListView, self).render_buttons(user, obj, **kwargs)
                    button_list.extend([
                        self.render_button(
                            url_name='edit_poll_permissions',
                            pk=obj.pk,
                            icon_classes='fa fa-lock',
                        ),
                        self.render_button(
                            btn_class='warning',
                            label='Button text',
                            icon_classes='glyphicon glyphicon-fire',
                            url=reverse('some_url_name_no_pk_required'),
                            condensed=False,
                        ),
                    ])
                    return button_list
    """
    search_form_class = None
    advanced_search_form_class = None

    def get_advanced_search_form_extra_kwargs(self):
        return {}

    def get_search_form_extra_kwargs(self):
        return {}

    def get_search_form(self):
        return self.search_form_class(self.request.GET or None,
                                      extra_kwargs=self.get_search_form_extra_kwargs())

    def get_advanced_search_form_class(self):
        querydict = self.request.GET.copy()
        querydict.pop('order_by', None)
        querydict.pop('page', None)

        if querydict and self.advanced_search_form_class:
            return self.advanced_search_form_class(self.request.GET,
                                                   extra_kwargs=self.get_advanced_search_form_extra_kwargs())
        elif self.advanced_search_form_class:
            return self.advanced_search_form_class(None,
                                                   extra_kwargs=self.get_advanced_search_form_extra_kwargs())
        return None

    def get_queryset(self):
        """Filters the default queryset based on self.search_form.search.

        Requires self.search_form to be set before this function is called,
        probably in self.get.

        If self.search_form is invalid, returns an empty list.
        """
        qs = super(CCESearchView, self).get_queryset()
        search_form = self.get_search_form()
        if search_form.is_valid():
            qs = search_form.search(qs)
        advanced_search_form = self.get_advanced_search_form_class()
        if advanced_search_form and advanced_search_form.is_valid():
            qs = advanced_search_form.search(qs)
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
    Variant of CCESearchView that downloads the search results as an xls or pdf report.

    Raises Http404 if the GET parameters do not form a valid search query.
    If no query string is specified, gives a report of all objects returned
    by get_queryset.

    The following fields must be defined on inheriting classes:
     - model or queryset (per BaseListView)
     - search_form_class (per SearchView)
     - report_function (see ReportView)
    """

    def get(self, request, *args, **kwargs):
        self.search_form = self.get_search_form()
        reports = self.get_reports()
        selected_report = request.GET.get('get_reports')
        if self.search_form.is_valid() and selected_report in reports:
            report = reports[selected_report]
            model = report['model'] if 'model' in report else self.model
            return getattr(model.reports, str('%s' % report['method']))(
                qs=self.get_queryset(),
                form=self.search_form
            )
        return super(ReportDownloadSearchView, self).get(request, *args, **kwargs)


class ReportDownloadDetailView(ReportDownloadView, CCEDetailView):
    """
    Variant of CCEDetailView that downloads the object as an xls or pdf report.
    """

    def get(self, request, *args, **kwargs):
        reports = self.get_reports()
        selected_report = request.GET.get('get_reports')
        if selected_report in reports:
            report = reports[selected_report]
            model = report['model'] if 'model' in report else self.model
            return getattr(model.reports, str('%s' % report['method']))(
                obj=self.get_object()
            )
        return super(ReportDownloadDetailView, self).get(request, *args, **kwargs)
