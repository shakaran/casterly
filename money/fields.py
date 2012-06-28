from decimal import Decimal

from django.db import models


class CurrencyField(models.DecimalField):
    """
    Custom field for a proper working with currencies. Using Decimal is not
    enough because it returns the value as a normal Python float, which
    is problematic when doing a lot of operations.
    """
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        try:
            return float(super(CurrencyField, self).to_python(
                value).quantize(Decimal("0.01")))
        except AttributeError:
            return None


# We need to give South some instructions about how to make
# the migrations properly
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^money\.models\.CurrencyField"])
