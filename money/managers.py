from calendar import monthrange
from datetime import date, timedelta

from django.db import models
from django.db.models.query import QuerySet
from isoweek import Week


class MovementQuerySet(QuerySet):

    def _amount(self, qs):
        return float(sum([value[0] for value in qs.values_list("amount")]))

    def expenses(self):
        return abs(self._amount(self.filter(amount__lt=0.0)))

    def earnings(self):
        return self._amount(self.filter(amount__gt=0.0))

    def balance(self):
        return self._amount(self.all())

    def per_month(self, year, month):
        _, last_day = monthrange(year, month)
        return self.filter(date__gte=date(year, month, 1),
            date__lte=date(year, month, last_day))

    def per_week(self, year, week):
        _week = Week(year, week)
        monday = _week.monday()
        sunday = monday + timedelta(6)
        return self.filter(date__gte=monday, date__lte=sunday)


class MovementManager(models.Manager):

    def per_month(self, year, month):
        return self.get_query_set().per_month(year, month)

    def per_week(self, year, week):
        return self.get_query_set().per_week(year, week)

    def get_query_set(self):
        return MovementQuerySet(self.model)

    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)
