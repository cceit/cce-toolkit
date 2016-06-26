import inspect
import operator

from django.db.models import Q

from toolkit.utils import replace_key


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
                q_filters.append(custom_field_lookup(self, queryset, value))
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

    def clean_range(
            self, range_start_field, range_end_field,
            range_start_error_message='End date must come after start date.',
            range_end_error_message='Start date must come before end date.',
            allow_equal=True,
            cleaned_data=None,
    ):
        """Make sure the given fields represent a valid range.

        NOTE: this method is really more of a procedure, as it directly
        modifies self._errors and self.cleaned_data (or the alternate
        cleaned_data dict,  if provided), rather than returning values for
        reassignment. Be sure to call it in the proper order with respect to
        other methods that make use of those dicts.

        This procedure was designed for use primarily with DateFields,
        reflected by the default error messages and allow_equal setting. It
        also works for other types of ranges, though; just specify different
        messages.

        Args:
            range_start_field: the name of the field holding the range start.
            range_end_field: the name of the field holding the range end.
            range_start_error_message: the error message to be added to the
            range start field if the range is invalid.
            range_end_error_message: the message to be added to the range end
            field if the range is invalid.
            allow_equal: if False, the range is considered invalid if its start
            and end are equal.
            cleaned_data: the dict of cleaned data to be updated. Uses
            self.cleaned_data by default.

        Side effects:
            - Deletes invalid field names from cleaned_data.
            - Modifies self._errors with appropriate error messages.
        """
        if cleaned_data is None:
            cleaned_data = self.cleaned_data
        start_value = cleaned_data.get(range_start_field)
        end_value = cleaned_data.get(range_end_field)
        if start_value and end_value:
            if start_value > end_value or not allow_equal \
                    and start_value == end_value:
                self._errors[range_start_field] = self.error_class(
                    [range_start_error_message]
                )
                self._errors[range_end_field] = self.error_class(
                    [range_end_error_message]
                )
                del cleaned_data[range_start_field]
                del cleaned_data[range_end_field]
