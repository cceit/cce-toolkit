from django.db.models import fields


class CurrencyField(fields.DecimalField):
    """Represents an amount of USD"""

    def __init__(self, max_digits=None, decimal_places=None, **kwargs):
        self.max_digits = max_digits or 12
        self.decimal_places = decimal_places or 2
        super(CurrencyField, self).__init__(**kwargs)
