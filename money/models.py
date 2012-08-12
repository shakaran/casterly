from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from money.fields import CurrencyField
from money.managers import MovementManager, SuggestionManager


AVAILABLE_ENTITIES = [
    ('lloyds', 'Lloyd\'s'),
    ('halifax', 'Halifax'),
]


class InvalidOperationError(Exception):
    pass


class BankAccount(models.Model):
    """
    Model for store information about personal bank accounts.
    """
    owner = models.ForeignKey(
        User,
        verbose_name=_(u'Owner'),
        related_name='bank_accounts',
    )
    description = models.CharField(
        verbose_name=_(u'Description'),
        help_text=_(u'Short description for identify the account'),
        max_length=50,
    )
    last_digits = models.CharField(
        verbose_name=_(u'Last 4 digits'),
        help_text=_(u'Insert the last 4 digits of your bank account'),
        max_length=4,
    )
    entity = models.CharField(
        verbose_name=_(u'Entity'),
        help_text=_(u'Entity for this account'),
        max_length=100,
        choices=AVAILABLE_ENTITIES,
        default=AVAILABLE_ENTITIES[0],
    )
    initial_balance = CurrencyField(
        verbose_name=_(u'Initial balance'),
        decimal_places=2,
        max_digits=7,
        default=0.0,
    )
    current_balance = CurrencyField(
        verbose_name=_(u'Current balance'),
        decimal_places=2,
        max_digits=7,
        default=0.0,
    )

    class Meta:
        verbose_name = _(u'Bank Account')
        verbose_name_plural = _(u'Bank Accounts')

    def __unicode__(self):
        return u'%s <****%s> - %0.2f' % (
            self.entity, self.last_digits, self.current_balance)


@receiver(signals.post_save, sender=BankAccount)
def set_current_balance(sender, instance, created, **kwargs):
    """
    Post-save signal for create a current balance in case that the
    user didn't provide any.
    """
    if created and instance.current_balance == 0.0:
        instance.current_balance = instance.initial_balance
        instance.save()


class MovementCategory(models.Model):
    """
    Simple model for be able to categorized movements.
    """
    name = models.CharField(
        verbose_name=_(u'Name'), max_length=200)

    class Meta:
        verbose_name = _(u'Movement category')
        verbose_name_plural = _(u'Movement categories')

    def __unicode__(self):
        return self.name


class Movement(models.Model):
    """
    Represents a movement into the account, in or out for the account.
    """
    bank_account = models.ForeignKey(
        BankAccount,
        verbose_name=_(u'Bank account'),
        related_name='movements',
    )
    category = models.ForeignKey(
        MovementCategory,
        verbose_name=_(u'Category'),
        blank=True,
        null=True,
        related_name='movements',
    )
    description = models.CharField(
        verbose_name=_(u'Description'),
        help_text=_(u'Short description for identify the movement'),
        max_length=50,
    )
    amount = CurrencyField(
        verbose_name=_(u'Amount'),
        decimal_places=2,
        max_digits=7,
    )
    current_balance = CurrencyField(
        verbose_name=_(u'Current balance'),
        decimal_places=2,
        max_digits=7,
        blank=True,
        null=True,
    )
    date = models.DateField(
        verbose_name=_(u'Date'),
    )

    objects = MovementManager()

    class Meta:
        verbose_name = _(u'Movement')
        verbose_name_plural = _(u'Movements')
        ordering = ('date', )

    def delete(self, *args, **kwargs):
        raise InvalidOperationError("Delete not allowed for this model")

    def __unicode__(self):
        return '%s - %s - %0.2f' % (
            self.bank_account.last_digits,
            self.date.strftime("%d/%m/%Y"),
            self.amount,
        )


class CategorySuggestion(models.Model):
    expression = models.CharField(
        verbose_name=_(u'Expression'),
        max_length=200,
    )
    category = models.ForeignKey(
        MovementCategory,
        verbose_name=_(u'Category'),
    )

    objects = SuggestionManager()

    class Meta:
        verbose_name = _(u'Category suggestion')
        verbose_name_plural = _(u'Category suggestions')

    def __unicode__(self):
        return u"%s - %s" % (self.expression, self.category.name)


@receiver(signals.post_save, sender=Movement)
def register_payment(sender, instance, created, **kwargs):
    """
    Post save signal for updating the bank account balance once we
    create a movement
    """
    if created:
        instance.bank_account.current_balance += instance.amount
        instance.bank_account.save()
        instance.current_balance = instance.bank_account.current_balance
        instance.save()
