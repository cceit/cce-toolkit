from django import forms
from django.forms import Select, SelectMultiple
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe

"""Based on django-select2-tags
https://github.com/jessamynsmith/django-select2-tags/blob/master/select2_tags/forms.py
"""


class Select2MultipleTagsWidget(SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<select data-tags="true" multiple="multiple"{}>', flatatt(final_attrs))]
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output))


class Select2TagsWidget(Select):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<select data-tags="true" {}>', flatatt(final_attrs))]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output))


class Select2FieldMixin(object):
    """ Handle creation of new values in (multiple) choice fields in the UI """
    def __init__(self, value_field, save_new=True, *args, **kwargs):
        """value_field is the field name in the model to be populated by new values entered in UI"""
        super(Select2FieldMixin, self).__init__(*args, **kwargs)
        self.value_field = value_field
        self.save_new = save_new
        self.new_items = set()

    def separate_new_values(self, values):
        self.new_items = set()
        key = self.to_field_name or 'pk'
        pk_values = []
        for pk in values:
            try:
                self.queryset.filter(**{key: pk})
                pk_values.append(pk)
            except (ValueError, TypeError):
                if pk:
                    self.new_items.add(pk)
        return pk_values

    def save_new_values(self):
        """
        Save any new values (tags) entered in the select2 box
        """
        if not self.save_new:
            raise ValueError('Should not call save_new_values when save_new is False')
        created_ids = []
        for item in self.new_items:
            create_kwargs = {self.value_field: item}
            new_object = self.queryset.model.objects.create(**create_kwargs)
            created_ids.append(new_object.pk)
        created_items = self.queryset.model.objects.filter(pk__in=created_ids)
        return created_items


class Select2TagsModelChoiceField(Select2FieldMixin, forms.ModelChoiceField):
    """
    Enables Select2 dropdown with tags option enabled to handle adhoc object creation

    :param string  value_field: the name of the field used to hold the select2 value on Foreign Model
    :param queryset queryset: the queryset used to population the ModelChoiceField

    Usage:
        .. code-block:: python
            :linenos:

            class PostForm(Select2TagsModelFormMixin, CCEModelForm):
                tags = Select2TagsModelChoiceField('name', queryset=Tag.objects.all())

    .. caution:: the widget does not load the necessary javascript files

    """

    widget = Select2TagsWidget
    def to_python(self, value):
        pk_values = self.separate_new_values([value])
        if pk_values:
            return super(Select2TagsModelChoiceField, self).to_python(value)
        return None


class Select2TagsModelMultipleChoiceField(Select2FieldMixin, forms.ModelMultipleChoiceField):
    """
    Enables Select2 multiple select with tags option enabled to handle adhoc object creation

    :param string  value_field: the name of the field used to hold the select2 value on Foreign Model
    :param queryset queryset: the queryset used to population the ModelChoiceField

    Usage:
        .. code-block:: python
            :linenos:

            class PostForm(Select2TagsModelFormMixin, CCEModelForm):
                tags = Select2TagsModelMultipleChoiceField('name', queryset=Tag.objects.all())

    .. caution:: the widget does not load the necessary javascript files

    """
    widget = Select2MultipleTagsWidget

    def _check_values(self, value):
        """
        Before calling super _check_values, set aside any values for new objects to be created
        """
        pk_values = self.separate_new_values(value)
        return super(Select2TagsModelMultipleChoiceField, self)._check_values(pk_values)


class Select2TagsModelFormMixin(object):
    """
    Enables saving of new values provides by the Select2Tags widgets

    Usage:
        .. code-block:: python
            :linenos:

            class PostForm(Select2TagsModelFormMixin, CCEModelForm):
                tags = Select2TagsModelMultipleChoiceField('name', queryset=Tag.objects.all())

    .. caution:: the widget does not load the necessary javascript files

    """

    def save(self, *args, **kwargs):
        instance = super(Select2TagsModelFormMixin, self).save(*args, **kwargs)
        dirty = False
        for field_name in self.fields:
            field = self.fields[field_name]
            if isinstance(field, Select2FieldMixin):
                if field.save_new:
                    new_values = field.save_new_values()
                    if new_values:
                        model_field = getattr(instance, field_name)
                        if isinstance(field, Select2TagsModelMultipleChoiceField):
                            model_field.add(*new_values)
                        else:
                            setattr(instance, field_name, new_values[0])
                            dirty = True
        if dirty:
            instance.save()
        return instance
