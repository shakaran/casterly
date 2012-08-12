from django.contrib import admin

from money.models import BankAccount, MovementCategory


class BankAccountAdmin(admin.ModelAdmin):
    pass


class MovementCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(MovementCategory, MovementCategoryAdmin)