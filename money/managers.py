from calendar import monthrange
from datetime import date, timedelta

from django.db import models
from django.db.models.query import QuerySet
from isoweek import Week


class MovementQuerySet(QuerySet):

    def _amount(self):
        return float(sum([value[0] for value in self.values_list("amount")]))

    def expenses(self):
        return abs(self.filter(amount__lt=0.0)._amount())

    def earnings(self):
        return abs(self.filter(amount__gt=0.0)._amount())

    def balance(self):
        return self.all()._amount()

    def per_month(self, year, month):
        _, last_day = monthrange(year, month)
        return self.filter(date__gte=date(year, month, 1),
            date__lte=date(year, month, last_day))

    def per_week(self, year, week):
        monday = Week(year, week).monday()
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
