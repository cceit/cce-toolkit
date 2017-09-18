from django.db.models import FileField, DecimalField
from django.utils.translation import ugettext_lazy as _


class CurrencyField(DecimalField):
    """Represents an amount of USD"""
    description = _("USD Currency value")

    def __init__(self, verbose_name=None, name=None, max_digits=None, decimal_places=None, **kwargs):
        super(CurrencyField, self).__init__(
            verbose_name, name, max_digits=(max_digits or 12), decimal_places=(decimal_places or 2),
            **kwargs
        )


class CleanFileField(FileField):
    def save_form_data(self, instance, data):
        # Important: None means "no change", false value means "clear"
        if data is not None:
            if not data:
                data = ''
                instance.delete()
            setattr(instance, self.name, data)
