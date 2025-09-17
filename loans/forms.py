from django import forms
from .models import Loan, Repayment


class loanApplicationForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['amount', 'interest_rate', 'term_months']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'interest_rate': forms.NumberInput(attrs={'step': '0.01'}),
            'term': forms.NumberInput(attrs={'min': 1}),
        }
        labels = {
            'amount': 'Loan Amount',
            'interest_rate': 'Interest Rate (%)',
            'term': 'Term (months)',
        }


class repaymentForm(forms.ModelForm):
    class Meta:
        model = Repayment
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'amount': 'Repayment Amount',
        }
