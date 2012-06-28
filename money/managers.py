from calendar import monthrange
from datetime import date

from django.db import models
from django.db.models.query import QuerySet


class MovementQuerySet(QuerySet):

    def _amount(self, qs):
        return float(abs(sum([value[0] for value
            in qs.values_list("amount")])))

    def expenses(self):
        return self._amount(self.filter(amount__lt=0.0))

    def earnings(self):
        return self._amount(self.filter(amount__gt=0.0))

    def balance(self):
        return self._amount(self.all())


class MovementManager(models.Manager):
    def get_query_set(self):
        return MovementQuerySet(self.model)

    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)

    def per_month(self, year, month):
        _, last_day = monthrange(year, month)
        return self.get_query_set().filter(
            date__gte=date(year, month, 1),
            date__lte=date(year, month, last_day))
