import os
from django.contrib.messages.views import SuccessMessageMixin as BuiltInSuccessMessageMixin
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.core.exceptions import ImproperlyConfigured, PermissionDenied


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
