from django.db.models import fields


class CurrencyField(fields.DecimalField):
    """Represents an amount of USD"""

    def __init__(self, **kwargs):
        self.max_digits = 12
        self.decimal_places = 2
        super(CurrencyField, self).__init__(**kwargs)
