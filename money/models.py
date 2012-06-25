from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class BankAccount(models.Model):
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
        help_text=_(u'Name of the entity for this account'),
        max_length=100,
    )
    initial_balance = models.DecimalField(
        verbose_name=_(u'Initial balance'),
        decimal_places=2,
        max_digits=7,
        default=0.0,
    )
    current_balance = models.DecimalField(
        verbose_name=_(u'Current balance'),
        decimal_places=2,
        max_digits=7,
        default=0.0,
    )

    class Meta:
        verbose_name = _('Bank Account')
        verbose_name_plural = _('Bank Accounts')

    def __unicode__(self):
        return u'%s <****%s> - %0.2f' % (
            self.entity,self.last_digits,self.current_balance)


@receiver(signals.post_save, sender=BankAccount)
def set_current_balance(sender, instance, created, **kwargs):
    if created and instance.current_balance == 0.0:
        instance.current_balance = instance.initial_balance
        instance.save()
