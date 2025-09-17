from django.contrib import admin
# Ensure Loan and Repayment are defined in models.py
from .models import Loan, Repayment

# Register your models here.


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'borrower', 'amount', 'interest_rate',
                    'balance', 'status', )
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('borrower__username', 'id', )


@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan', 'amount',
                    'payment_date', 'is_penalty', )
    list_filter = ('is_penalty', 'payment_date', )
