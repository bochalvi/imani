from django import forms
from .models import SavingsAccount, Transaction


class SavingsAccountForm(forms.ModelForm):
    class Meta:
        model = SavingsAccount
        exclude = ['current_balance', 'last_activity']


class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'amount', 'description']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'amount', 'description']


class AccountCreationForm(forms.ModelForm):
    class Meta:
        model = SavingsAccount
        # These will be set automatically
        exclude = ['account_number', 'member']
