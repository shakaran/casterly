from django.contrib import admin

from money.models import BankAccount


class BankAccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(BankAccount, BankAccountAdmin)