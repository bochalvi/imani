from django.db import models
from members.models import Member
from .utils import generate_account_number
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()


class SavingsAccount(models.Model):
    ACCOUNT_TYPES = [
        ('REG', 'Regular Savings'),
        ('FIX', 'Fixed Deposit'),
        ('TAR', 'Target Savings'),
        ('ADJ', 'Adjustment')
    ]

    account_number = models.CharField(max_length=20, unique=True)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    account_type = models.CharField(max_length=3, choices=ACCOUNT_TYPES)
    opening_date = models.DateField(auto_now_add=True)
    current_balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=0)
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    last_activity = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.account_number:  # Generate account number only for new instances
            self.account_number = generate_account_number(self.account_type)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account_number} - {self.member}"

    def get_total_deposits(self):
        return self.transaction_set.filter(transaction_type='DEP').aggregate(total=models.Sum('amount'))['total'] or 0

    def get_total_withdrawals(self):
        return self.transaction_set.filter(transaction_type='WTH').aggregate(total=models.Sum('amount'))['total'] or 0


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEP', 'Deposit'),
        ('WTH', 'Withdrawal'),
        ('INT', 'Interest'),
    ]

    account = models.ForeignKey(SavingsAccount, on_delete=models.PROTECT)
    transaction_type = models.CharField(
        max_length=3, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    reference_number = models.CharField(max_length=50, unique=True)
    processed_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        # Update account balance when saving transaction
        if not self.pk:  # Only for new transactions
            account = self.account
            if self.transaction_type in ['DEP', 'INT']:
                account.current_balance += self.amount
            elif self.transaction_type in ['WTH', 'ADJ']:
                account.current_balance -= self.amount
            account.save()
        super().save(*args, **kwargs)

    def get_balance(self):
        """Returns the current balance"""
        return self.current_balance


def update_balance(self):
    """Recalculates balance from all transactions"""
    deposits = self.transactions.filter(
        transaction_type__in=['DEP', 'INT']
    ).aggregate(total=models.Sum('amount'))['total'] or 0

    withdrawals = self.transactions.filter(
        transaction_type__in=['WTH', 'ADJ']
    ).aggregate(total=models.Sum('amount'))['total'] or 0

    self.current_balance = deposits - withdrawals
    self.save()
    return self.current_balance

    def __str__(self):
        return f"{self.reference_number} - {self.get_transaction_type_display()}"


def account_details(self):
    """Returns a string representation of the account details"""
    if not self.account_number:
        return "Account number not set"
    if not self.member:
        return "Member not assigned to this account"
    return f"Account: {self.account_number}, Type: {self.get_account_type_display()}, Balance: {self.current_balance}"


class SavingsGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(upload_to='group_logos/', blank=True, null=True)
    monthiy_target = models.DecimalField(
        max_digits=15, decimal_places=2, default=0)
    meeting_schedule = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
