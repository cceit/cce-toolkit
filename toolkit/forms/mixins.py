import inspect
import operator

from django.db.models import Q

from toolkit.helpers.utils import replace_key


class SearchFormMixin(object):
    """
    Mixin used to create a search form. Allows you to define a list of
    field-filters pairs used to filter the queryset passed to the form

    filters can be a combination of list of fields, Q objects
    and custom filter methods


    """
    def filters(self, queryset):
        """
        Prepares the dictionary of queryset filters based on the form cleaned
        data

        :param Queryset queryset: the queryset to filter through.

        :returns: tuple of q_objects and kwargs used in filtering the queryset

        .. warning:: method uses cleaned_data, self.full_clean() must be
         called first.
        """
        # Exclude None and empty collections and strings, but include False
        # and 0 (valid filter values).
        kwargs = {field_name: value
                  for field_name, value in self.cleaned_data.items()
                  if value or value is False or value == 0}
        q_objects = []
        q_filters = []
        for field_name, custom_field_lookup \
                in self.Meta.field_lookups.iteritems():
            value = self.cleaned_data[field_name]

            if inspect.isfunction(custom_field_lookup):
                processed_filters = custom_field_lookup(self, queryset, value)
                if type(processed_filters) is list:
                    q_filters.extend(processed_filters)
                else:
                    q_filters.append(processed_filters)
                if field_name in kwargs:
                    kwargs.pop(field_name)
            if type(custom_field_lookup) is tuple:
                # if its tuple of field_lookups, remove the field name lookup
                # from filters and add a new Q Object filter for each field
                # lookup in the tuple then reduce the list of Q objects using
                # the OR operator

                if value:
                    if field_name in kwargs:
                        kwargs.pop(field_name)
                    q_field_lookups = []

                    for field_lookup in custom_field_lookup:
                        q_field_lookups.append(
                            Q(**{'%s' % field_lookup: value}))

                    q_obj = reduce(operator.or_, q_field_lookups)

                    q_filters.append(q_obj)
            else:
                # replace the default field name field lookup with the custom
                # field lookup
                kwargs = replace_key(field_name, custom_field_lookup, kwargs)
        if q_filters:
            q_objects = reduce(operator.and_, q_filters)

        return q_objects, kwargs

    def search(self, queryset):
        """Filter the given queryset according to the form's cleaned data.

         .. warning:: self.full_clean() must be called first.

        :param Queryset queryset: the queryset to filter through.

        :returns: filtered version of the initial queryset.

        :raises: AttributeError, if the form is not valid.
        """
        q_objects, kwargs = self.filters(queryset)
        if q_objects:
            queryset = queryset.filter(q_objects)
        if kwargs:
            queryset = queryset.filter(**kwargs)
        return queryset.distinct()