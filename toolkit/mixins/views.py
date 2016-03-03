import copy
import os
from collections import OrderedDict
from django.contrib.messages.views import SuccessMessageMixin as BuiltInSuccessMessageMixin
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from django.contrib.admin.utils import NestedObjects


class SuccessMessageMixin(BuiltInSuccessMessageMixin):
    """
    Use when you'd like a success message added to your Create or Update response.
    Assumptions:
        - Class has method form_valid()
    Limitations:
        - Class cannot override form_valid()
        - Success message may only be one line.

    Use when you'd like a success message added to your Delete response.
    Assumptions:
        - Class has method delete()
    Limitations:
        - Class cannot override delete()
        - Success message may only be one line.
    """

    def dispatch(self, request, *args, **kwargs):
        if not self.success_message:
            raise NotImplementedError(
                "You must define the 'success_message' property."
            )

        return super(SuccessMessageMixin, self).dispatch(request, *args, **kwargs)

    def forms_valid(self, form, inlines, *args, **kwargs):
        response = super(SuccessMessageMixin, self).forms_valid(form, inlines, *args, **kwargs)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def delete(self, request, *args, **kwargs):
        response = super(SuccessMessageMixin, self).delete(request, *args, **kwargs)
        success_message = self.get_success_message({})
        if success_message:
            messages.success(self.request, success_message)
        return response

    def formset_valid(self, formset, *args, **kwargs):
        response = super(SuccessMessageMixin, self).formset_valid(formset, *args, **kwargs)
        success_message = self.get_success_message({})
        if success_message:
            messages.success(self.request, success_message)
        return response


def append_object(model, context_variable_name, field_lookup):
    if type(field_lookup) is not dict:
        field_lookup = {"pk": field_lookup}

    def get_filters(**kwargs):
        return {
            k: kwargs[v]
            for k, v
            in field_lookup.items()
        }

    def get_instance(**kwargs):
        # TODO: try/except on key error, reraise with a more helpful error
        filters = get_filters(**kwargs)
        return model.objects.get(**filters)

    return model, context_variable_name, field_lookup, get_instance


class AppendURLObjectsMixin(object):
    """
    this mixin is used to get and append objects, who's pks are passed in view kwargs making the objects available
    to all the methods in your view as well your template.
    To use this mixin, you need to set the append_objects property with a list of tuples each containing 3 values

    append_object format: (Model, context_variable_name, field_lookup)
    example 1: append_objects = [(Course, 'course', 'course_pk'), (Student, 'student', 'student_pk')]
    in this example, the mixin will try to get the Course and Student objects based on course_pk and student_pk which
    are passed through the view url. This mixin assumes that the value being passed by field_lookup contains
    the pk of the object you're trying to fetch. The fetched objects will be appended to context data with variables
    named after the second value in the triple ('course' or 'student')

    example 2: append_objects = [(Course, 'course', 'course_pk'), (Student, 'student', {'student_id': 'student_pk'})]
    In this example, we pass a dict in the field_lookup parameter which represents a mapping of model field lookup
    method and values that will be passed in the url.

    the mixin will raise 404 exception if any object is not found
    """
    make_append_object = staticmethod(append_object)
    append_objects = None

    def append_from_kwargs(self):
        if not self.append_objects:
            raise NotImplementedError(
                "You must define the 'append_objects' property. "
                "Format: append_objects = "
                "[AppendURLObjectsMixin.make_append_object(Model, context_variable_name, field_lookup)] "
            )

        for appended_object in self.append_objects:
            if isinstance(appended_object, tuple):
                if 3 is len(appended_object):
                    # brittle; try not to rely on that
                    appended_object = self.make_append_object(*appended_object)
            appended_model = appended_object[0]
            context_name = appended_object[1]
            if hasattr(self, context_name):
                raise Exception(
                    "The following context variable name collides with other class properties, "
                    "please user a different name: %s" % context_name
                )
            try:
                instance = appended_object[3](**self.kwargs)
            except appended_model.DoesNotExist:
                raise Http404('No %s matches the given query.' % appended_model._meta.object_name)
            setattr(self, context_name, instance)

    def dispatch(self, request, *args, **kwargs):
        self.append_from_kwargs()
        return super(AppendURLObjectsMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AppendURLObjectsMixin, self).get_context_data(**kwargs)
        for appended_object in self.append_objects:
            appended_name = appended_object[1]
            context.update({appended_name: getattr(self, appended_name)})
        return context


class PermissionsRequiredMixin(object):
    """
    Inspired by django-braces: https://github.com/brack3t/django-braces

    Requires django-rulez https://github.com/chrisglass/django-rulez
    TODO: Does this actually require django-rulez anymore?

    Parent class of view mixins which allow you to specify a list of rules for
    access to a resource (model or instance of a model, currently)
    via django-rulez by http verb.  Each permission
    that is listed will be required (logical AND for multiple cce_permissions).

    A 403 will be raised if any of the checks fails.

    Simply create a dictionary with http verbs as keys, and
    each of their values should be a list of functions (as strings)
    in 'function_name' format.  Each permission should be a function
    in the same class as the model or model instance defined on
    the view that inherits one of the children mixins.

    Example Usage on an UpdateView subclass:

        cce_permissions = {
            "get": ["add_object"]
            "post": ["change_object", "delete_object"]
            }

    """
    permissions = None  # Default required perms to none

    def dispatch(self, request, *args, **kwargs):
        # some things we use, like get_object(), need the following
        self.kwargs = kwargs

        # sanity checks
        self._check_permissions_attr()
        self._check_perms_keys()
        self._check_resource()

        # check perms here
        if request.method.lower() in self.permissions.keys():
            for func in self.permissions.get(request.method.lower()):
                self._check_permissions(request, func)

        return super(PermissionsRequiredMixin, self).dispatch(
            request, *args, **kwargs)

    def _check_permissions(self, request, permission):
        """
        This method is responsible for calling the permission
        checking functions.
        """
        raise NotImplementedError(
            "You must define and implement a '_check_permissions' method"
        )

    def _check_resource(self):
        """
        This method is responsible for calling the implementing mixin's
        method that verifies the resource is defined; aka get_object()
        or model exists.
        """
        raise NotImplementedError(
            "You must define and implement a '_check_resource' method"
        )

    def _check_permissions_attr(self):
        """
        This method checks that the cce_permissions attribute
        is set and that it is a dict.
        """
        if self.permissions is None or not isinstance(self.permissions, dict):
            raise ImproperlyConfigured(
                "'PermissionsRequiredMixin' requires "
                "'cce_permissions' attribute to be set to a dict.")

    def _check_perms_keys(self):
        """
        This method checks that the listed permission checking functions
        on the resources exist.
        """
        raise NotImplementedError(
            "You must implement a _check_perms_keys method"
        )


class ObjectPermissionsMixin(PermissionsRequiredMixin):
    """
    Use this mixin when get_object() is called in your view;
    i.e. DetailView, UpdateView, etc.

    This class should implement three methods:

    _check_resource()
        should verify that the resource we wish to protect
        (object, model, etc.) exists

    _check_perms_keys()
        should verify that the permission functions exist

    _check_permissions()
        should actually make the call to the defined cce_permissions
    """

    def _check_permissions(self, request, permission):
        resource = self.get_object()
        permission_func = getattr(resource, permission)
        if not permission_func(request.user):
            raise PermissionDenied

    def _check_resource(self):
        self._check_get_object()

    def _check_perms_keys(self):
        """
        If the cce_permissions list/tuple passed in is set, check to make
        sure that it is of the type list or tuple.
        """
        for k, v in self.permissions.iteritems():
            if not v:
                raise ImproperlyConfigured(
                    "'PermissionsRequiredMixin' requires"
                    "'cce_permissions' functions list to have at least one item.")
            for func in v:
                if getattr(self.get_object(), func, None) is None:
                    raise ImproperlyConfigured(
                        "Cannot locate %s.%s; does it exist?" % (self.get_object(), func))

    def _check_get_object(self):
        """
        Make sure get_object exists
        """
        if getattr(self, 'get_object', None) is None:
            raise ImproperlyConfigured(
                "'ObjectPermissionsMixin' requires a get_object method"
            )


class ClassPermissionsMixin(PermissionsRequiredMixin):
    """
    Use this mixin when table-level cce_permissions are required;
    i.e. CreateView, etc.

    This class should implement three methods:

    _check_resource()
        should verify that the resource we wish to protect
        (object, model, etc.) exists

    _check_perms_keys()
        should verify that the permission functions exist

    _check_permissions()
        should actually make the call to the defined cce_permissions
    """

    def _check_permissions(self, request, permission):
        resource = self.model()
        permission_func = getattr(resource, permission)
        if not permission_func(request.user):
            raise PermissionDenied

    def _check_resource(self):
        self._check_model()

    def _check_perms_keys(self):
        """
        If the cce_permissions list/tuple passed in is set, check to make
        sure that it is of the type list or tuple.
        """
        for k, v in self.permissions.iteritems():
            if not v:
                raise ImproperlyConfigured(
                    "'PermissionsRequiredMixin' requires"
                    "'cce_permissions' functions list to have at least one item.")
            for func in v:
                if getattr(self.model, func, None) is None:
                    raise ImproperlyConfigured(
                        "Cannot locate %s.%s; does it exist?" % (self.model, func))

    def _check_model(self):
        """
        Make sure model is defined on CBV
        """
        if getattr(self, 'model', None) is None:
            raise ImproperlyConfigured(
                "'ObjectPermissionsMixin' requires a model attribute"
                "to be defined on the class"
            )


class ViewMetaMixin(object):
    """
    Mixin will be used capture optional and required meta data about each view that are then passed to the template

    """
    page_title = ''
    page_headline = ''
    sidebar_group = []

    def get_page_title(self):
        if not self.page_title:
            raise ImproperlyConfigured("page_title is not set")
        return self.page_title

    def get_page_headline(self):
        return self.page_headline or self.get_page_title()

    def get_sidebar_group(self):
        if not self.sidebar_group:
            raise ImproperlyConfigured("sidebar_group is not set")
        return self.sidebar_group

    def get_context_data(self, **kwargs):
        context = super(ViewMetaMixin, self).get_context_data(**kwargs)
        context.update({
            'page_title': self.get_page_title(),
            'page_headline': self.get_page_headline(),
            'sidebar_group': self.get_sidebar_group(),
        })
        return context


class FileDownloadMixin(object):
    """
    View mixin to make that view return a file from a model field on GET.
    Views using this mixin must implement the method get_file_field_to_download.
    Note: This is for serving a file as a response and is no longer recommended.
    """
    def get(self, *args, **kwargs):
        # This view will directly stream the file with the content-disposition of an attachment
        backing_file = self.get_file_field_to_download()

        # taken from http://subversion.outreach.cce/svn/it/django/sooner_flight/trunk/content_repository/views.py
        if not backing_file:
            raise Http404("The resource requested is no longer available")
        response = HttpResponse()

        # http://stackoverflow.com/questions/9421797/django-filefield-open-method-returns-none-for-valid-file
        backing_file.open()  # TODO: check for IOError

        # TODO: get the content length
        file_contents = backing_file.read()
        backing_file.close()
        response.write(file_contents)
        response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(backing_file.name)
        return response


class AbstractedListMixin(object):
    """
    Assumes that it's mixed in with a ListView that has self.model.
    """
    template_name = "generic_list.html"
    columns = None
    popover_rows = None
    actions_column_width = '1'  # will be coerced to a string and put into a Bootstrap class.

    def render_button(self, pk=None, btn_class='', url_name='', label='', icon_classes='', button_text='', url=''):
        """
        Takes of boatload of parameters and returns the HTML for a nice Bootstrap button-link.
        If the URL lookup fails, no button is returned.

        Must have EITHER pk and url_name OR url.
        """
        if not url:
            try:
                url = reverse(url_name, kwargs={'pk': pk})
            except NoReverseMatch:
                return None
        return btn_class, url, label, icon_classes, button_text

    def render_buttons(self, user, obj, view_perm_func=None, edit_perm_func=None, delete_perm_func=None):
        """
        This method provides default buttons for an object in a ListView: View, Edit and Delete.
        The default permission functions are can_view, can_update and can_delete.
        We can depend on all three of these permissions methods being there because of CCEAuditModel.
        Other permission functions can be passed, though this is unlikely to happen under the current structure.
        If a URL is not found, or if the user doesn't have permission to do that thing, the button is not rendered.
        """
        buttons = []
        underscored_model_name = '_'.join(self.model._meta.verbose_name.lower().split(' '))
        if view_perm_func is None:
            view_perm_func = self.model.can_view
        if view_perm_func(obj, user):
            button = self.render_button(obj.pk, 'btn-info', 'view_'+underscored_model_name, 'View', 'glyphicon glyphicon-info-sign')
            if button:
                buttons.append(button)
        if edit_perm_func is None:
            edit_perm_func = self.model.can_update
        if edit_perm_func(obj, user):
            button = self.render_button(obj.pk, 'btn-warning', 'edit_'+underscored_model_name, 'Edit', 'glyphicon glyphicon-edit')
            if button:
                buttons.append(button)
        if delete_perm_func is None:
            delete_perm_func = self.model.can_delete
        if delete_perm_func(obj, user):
            button = self.render_button(obj.pk, 'btn-danger', 'delete_'+underscored_model_name, 'Delete', 'glyphicon glyphicon-remove')
            if button:
                buttons.append(button)
        return buttons

    def get_columns(self):
        if self.columns is None:
            # This error is caught in get_context_data so that ListViews that don't use this abstraction don't blow up.
            raise NotImplementedError
        return self.columns

    def get_popover_rows(self):
        if self.popover_rows is None:
            # This error is caught in get_context_data so that ListViews that don't use this abstraction don't blow up.
            raise NotImplementedError
        return self.popover_rows

    def generate_list_view_table(self, columns, data):
        """
        Generates a data structure for use in the generic list template.
        The "columns" parameter is a list of 2-tuples or 3-tuples. These contain
        - a column title,
        - EITHER a function that takes one parameter (an object from the list) and returns a cell of data
          OR a dot-separated string of attributes, and
        - an optional column width number that will go into a Bootstrap class.
        All of these values will be coerced to strings in the template. So the function can return an object, and its
        string representation will be used. The column width can be a string or an integer.
        Example:
        columns = [
            ("Column title", lambda obj: obj.method_name(CONSTANT)),
            ("Other title", previously_defined_function, '3'),
            ("Third", 'dotted.attribute', 2),
        ]
        The "data" parameter should be an iterable.
        This method returns a data structure of the following form (using the above example as input):
        [
            [("Column title", ''), ("Other title", '3'), ("Third", 2)],
            [data[0].method_name(CONSTANT), previously_defined_function(data[0]), data[0].dotted.attribute],
            [data[1].method_name(CONSTANT), previously_defined_function(data[1]), data[1].dotted.attribute],
            # etc.
        ]
        """
        titles, functions = [], []
        columns = list(columns)
        if columns:
            new_columns = []
            for tupple in columns:
                # deal with column widths
                if len(tupple) == 2:
                    tupple = tupple + ('',)
                elif len(tupple) == 3:
                    pass
                else:
                    continue  # throw out bad rows
                new_columns.append(tupple)
            # Now each tuple in new_columns is (title, function, number or empty string)
            titles, functions, column_widths = zip(*new_columns)
            titles = zip(titles, column_widths)
        table = [titles]
        for obj in data:
            row = []
            for f in functions:
                if type(f) == str:
                    new_obj = obj
                    attrs = f.split('.')
                    for attr in attrs:
                        if hasattr(new_obj, attr):
                            new_obj = getattr(new_obj, attr)
                        else:
                            raise Exception("Bad dotted attributes passed to %s: %s" % (type(new_obj), f))
                    row.append(new_obj)
                else:
                    row.append(f(obj))
            table.append(row)
        return table

    def generate_popover_media(self, rows, data):
        row_titles, functions = [], []
        rows = list(rows)
        if rows:
            new_rows = [row for row in rows]
            # Now each tuple in new_columns is (title, function)
            row_titles, functions = zip(*new_rows)
        popover_dict = {}
        row_values = []
        for obj in data:
            row = []
            for f in functions:
                if type(f) == str:
                    new_obj = obj
                    attrs = f.split('.')
                    for attr in attrs:
                        if hasattr(new_obj, attr):
                            new_obj = getattr(new_obj, attr)
                        else:
                            raise Exception("Bad dotted attributes passed to %s: %s" % (type(new_obj), f))
                    if isinstance(new_obj, models.Manager):
                        objs_repr = ', '.join([str(o) for o in new_obj.all()])
                        row.append(objs_repr)
                    else:
                        row.append(new_obj)
                else:
                    row.append(f(obj))
            row_values.append(row)
        popover_dict[row_titles] = row_values
        return popover_dict

    def get_context_data(self, **kwargs):
        """
        Puts things into the context that the template needs:
        - the message to display when there are no results in the list
        - the context menu template name (calculated from the model name)
        - the table of data from generate_list_view_table
        """
        context = super(AbstractedListMixin, self).get_context_data(**kwargs)
        try:
            columns = copy.copy(self.get_columns())
        except NotImplementedError:
            # If self.columns was not defined, just return the super context
            return context
        qs = context['object_list']  # this works whether the view is paginated or not
        try:
            popover_rows = copy.copy(self.get_popover_rows())
        except NotImplementedError:
            # Popover is optional
            quicklook = None
        else:
            quicklook = self.generate_popover_media(rows=popover_rows, data=qs)
        # If we didn't use copy above, this next line would keep adding Actions columns every time the page is accessed
        columns += [('Actions', lambda x: self.render_buttons(self.request.user, x), self.actions_column_width)]
        meta = self.model._meta
        table = self.generate_list_view_table(columns=columns, data=qs)
        underscored_model_name = '_'.join(meta.verbose_name.lower().split(' '))
        context.update({
            'empty_list_message': 'No %s found.' % meta.verbose_name_plural,
            'context_menu_template': '%s/context_menu.html' % underscored_model_name,
            'table': table,
            'quicklook': quicklook,
        })
        return context


class AbstractedDetailMixin(object):
    """
    Assumes that it's mixed in with a DetailView that has self.model and self.get_object().
    """
    template_name = "generic_detail.html"
    detail_fields = None

    def get_details(self):
        """
        How self.fields should be formatted:
        - The first item in each tuple should be the label.
        - The second item should be EITHER a dotted path from this object to what goes on the page,
          OR a function that takes exactly one argument.
        - The third item is an optional extra parameter.
        - - If the thing passed is a related manager, this is an optional dotted path to apply to each object in the manager.
        Example:
        fields = [
            ('Username', 'user.username'),
            ('Passport file', 'passport'),
            ('Zip codes', 'address_set', 'zip_code'),
            ('Active', 'is_active'),
            ('Joined date', 'joined_date'),
            ('Type', lambda obj: type(obj)),
        ]
        Returns an OrderedDict of {label: (value, param)} that gets dropped into the template.
        """
        def follow_path(ob, dotted_attrs):
            new_ob = ob
            attrs = dotted_attrs.split('.')
            for attr in attrs:
                if hasattr(new_ob, attr):
                    new_ob = getattr(new_ob, attr)
                    if callable(new_ob) and not isinstance(new_ob, models.Manager):
                        new_ob = new_ob()
                else:
                    raise Exception("Bad dotted attributes passed to %s: %s" % (type(new_ob), dotted_attrs))
            return new_ob

        details = OrderedDict()
        if not self.detail_fields:
            return details
        obj = self.get_object()
        for tupple in self.detail_fields:
            label = tupple[0]
            dotted_or_function = tupple[1]
            param = tupple[2] if len(tupple) > 2 else None

            if callable(dotted_or_function):
                new_obj = dotted_or_function(obj)
            else:
                new_obj = follow_path(obj, dotted_or_function)
            details[label] = (new_obj, param)
        return details

    def get_context_data(self, **kwargs):
        context = super(AbstractedDetailMixin, self).get_context_data(**kwargs)
        meta = self.model._meta
        underscored_model_name = '_'.join(meta.verbose_name.lower().split(' '))
        context.update({
            'context_menu_template': '%s/context_menu.html' % underscored_model_name,
            'details': self.get_details(),
        })
        return context


class AbstractedDeleteMixin(object):
    template_name = "generic_delete.html"

    @staticmethod
    def get_deleted_objects(objs, using):
        """
        Find all objects related to ``objs`` that should also be deleted. ``objs``
        must be a homogeneous iterable of objects (e.g. a QuerySet).

        Returns a nested list of objects suitable for display in the
        template with the ``unordered_list`` filter.

        This is simplified from a method by the same name that the Django admin uses.
        "using" means the key in the DATABASES setting.
        """
        collector = NestedObjects(using=using)
        collector.collect(objs)
        to_delete = collector.nested()  # nested() can take a formatting callback if we want it later
        return to_delete

    def get_context_data(self, **kwargs):
        context = super(AbstractedDeleteMixin, self).get_context_data(**kwargs)
        obj = self.get_object()
        # Get a queryset so that we can get the database alias
        db_alias = self.model.objects.filter(pk=obj.pk).db
        objs_to_be_deleted = AbstractedDeleteMixin.get_deleted_objects([obj], db_alias)
        object_name = self.model._meta.verbose_name
        underscored_model_name = '_'.join(self.model._meta.verbose_name.lower().split(' '))
        context.update({
            'object_name': object_name,
            'no_url_path': reverse('view_%s' % underscored_model_name, kwargs={'pk': obj.pk}),
            'objs_to_be_deleted': objs_to_be_deleted,
        })
        return context


class ContextMenuMixin(object):
    show_context_menu = False

    def get_verbose_names(self):
        return self.model._meta.verbose_name.lower(), self.model._meta.verbose_name_plural.lower()

    def get_underscored_names(self):
        verbose_name = self.model._meta.verbose_name.lower()
        verbose_name_plural = self.model._meta.verbose_name_plural.lower()
        return '_'.join(verbose_name.split(' ')), '_'.join(verbose_name_plural.split(' '))

    def get_context_data(self, **kwargs):
        context = super(ContextMenuMixin, self).get_context_data(**kwargs)
        if hasattr(self, 'show_context_menu'):
            context['show_context_menu'] = self.show_context_menu
        else:
            context['show_context_menu'] = False
        if hasattr(self, 'context_menu_items'):
            context['context_menu_items'] = self.context_menu_items()
        else:
            context['context_menu_items'] = []
        context['verbose_name_plural'] = str(self.model._meta.verbose_name_plural).title()
        return context


class ListContextMenuMixin(ContextMenuMixin):
    def context_menu_items(self):
        if not self.show_context_menu:
            return []
        name, plural_name = self.get_verbose_names()
        name_underscored, plural_underscored = self.get_underscored_names()
        menu_links = []
        # label, reversed url, icon class, sidebar_group
        try:
            add_url = reverse("add_%s" % name_underscored)
        except NoReverseMatch:
            pass
        else:
            menu_links.append(
                ("Add %s" % name.title(), add_url, "glyphicon-plus", "add_%s" % name_underscored)
            )
        return menu_links


class DetailContextMenuMixin(ContextMenuMixin):
    def context_menu_items(self):
        if not self.show_context_menu:
            return []
        name, plural_name = self.get_verbose_names()
        name_underscored, plural_underscored = self.get_underscored_names()
        menu_links = []
        try:
            edit_url = reverse("edit_%s" % name_underscored, kwargs={'pk': self.get_object().pk})
        except NoReverseMatch:
            pass
        else:
            menu_links.append(
                ("Edit %s" % name.title(), edit_url, "glyphicon-edit", "edit_%s" % name_underscored),
            )
        return menu_links


class CreateContextMenuMixin(ContextMenuMixin):
    def context_menu_items(self):
        if not self.show_context_menu:
            return []
        name, plural_name = self.get_verbose_names()
        name_underscored, plural_underscored = self.get_underscored_names()
        menu_links = []
        try:
            browse_url = reverse("browse_%s" % plural_underscored)
        except NoReverseMatch:
            pass
        else:
            menu_links.append(
                ("Browse %s" % plural_name.title(), browse_url, "glyphicon-list")
            )
        return menu_links


class UpdateContextMenuMixin(ContextMenuMixin):
    def context_menu_items(self):
        if not self.show_context_menu:
            return []
        name, plural_name = self.get_verbose_names()
        name_underscored, plural_underscored = self.get_underscored_names()
        menu_links = []
        try:
            view_url = reverse("view_%s" % name_underscored, kwargs={'pk': self.get_object().pk})
        except NoReverseMatch:
            pass
        else:
            menu_links.append(
                ("View %s" % name.title(), view_url, "glyphicon-info-sign")
            )
        return menu_links
