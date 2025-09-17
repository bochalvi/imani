from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.


class Loan(models.Model):
    LOAN_STATUS = [
        ('pending', 'Pending Approval'),
        ('approved', 'Active'),
        ('rejected', 'Rejected'),
        ('Paid', 'Fully Paid'),
        ('defaulted', 'Defaulted'),
        ('cancelled', 'Cancelled'),
        ('in_progress', 'In Progress'),
    ]
    borrower = models.ForeignKey(User, on_delete=models.CASCADE,)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[
                                 MinValueValidator(100)])
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    term_months = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])
    disbursement_date = models.DateTimeField(null=True, blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    rejected_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=LOAN_STATUS, default='pending')
    # balance field removed to avoid conflict with balance property
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def balance(self):
        repayments = self.repayment_set.all().aggregate(total=models.Sum('amount'))
        paid = repayments['total'] if repayments['total'] else 0
        return self.amount + self.total_interest - paid

    @property
    def total_interest(self):
        return (self.amount * self.interest_rate * self.term_months) / (100 * 12)

    @property
    def monthly_payment(self):
        if self.term_months == 0:
            return 0
        r = self.interest_rate / 100 / 12
        return (self.amount * r * (1 + r) ** self.term_months) / ((1 + r) ** self.term_months - 1)

    @property
    def is_active(self):
        return self.status == 'approved' and self.balance > 0

    @property
    def is_pending(self):
        return self.status == 'pending'

    @property
    def is_rejected(self):
        return self.status == 'rejected'

    @property
    def is_paid(self):
        return self.status == 'Paid'

    @property
    def is_defaulted(self):
        return self.status == 'defaulted'

    @property
    def is_cancelled(self):
        return self.status == 'cancelled'

    @property
    def is_in_progress(self):
        return self.status == 'in_progress'

    def __str__(self):
        return f"Loan #{self.id} - {self.borrower.username}"


PAYMENT_METHODS = [
    ('cash', 'Cash'),
    ('bank', 'Bank Transfer'),
    ('mobile', 'Mpesa/Airtel Money'),
]


class Repayment(models.Model):

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHODS, default='cash')
    payment_date = models.DateTimeField(auto_now_add=True)
    is_penalty = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.loan.balance <= 0:
            self.loan.status = 'Paid'
            self.loan.save()

    @property
    def date_paid(self):
        return self.payment_date.strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return f"Repayment ${self.amount} for Loan #{self.loan.id}"
