from django.contrib import admin
from .models import SavingsAccount, Transaction, SavingsGroup


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0


@admin.register(SavingsAccount)
class SavingsAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'member',
                    'account_type', 'current_balance')
    list_filter = ('account_type', 'is_active')
    search_fields = ('account_number', 'member__first_name',
                     'member__last_name')
    inlines = [TransactionInline]
    readonly_fields = ('account_number',)  # Prevent manual editing


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'account',
                    'transaction_type', 'amount', 'transaction_date')
    list_filter = ('transaction_type', 'transaction_date')
    search_fields = ('reference_number', 'account__account_number')
# Register your models here.


@admin.register(SavingsGroup)  # Ensure SavingsGroup is defined in models.py
class savingsGroupAdmin(admin.ModelAdmin):
    list_display = ('name',  'created_at')
    search_fields = ('name',)


class Meta:
    model = SavingsGroup
    fields = ('name', 'description', 'logo', 'monthiy_target',
              'meeting_schedule', 'is_active')
    readonly_fields = ('created_at',)  # Prevent manual editing of created_at
