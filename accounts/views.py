from accounts.models import SavingsGroup
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
import time
from django.contrib import messages
from .models import SavingsAccount, Transaction
from .forms import SavingsAccountForm, DepositForm, WithdrawalForm, AccountCreationForm
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, permission_required
from members.models import Member
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

# Ensure SavingsGroup exists in members/models.py or remove this line if not used
from members.models import Member


@login_required
def account_list(request):
    accounts = SavingsAccount.objects.filter(is_active=True)
    return render(request, 'account_list.html', {'accounts': accounts})


@login_required
@permission_required('accounts.add_savingsaccount', raise_exception=True)
def create_account(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == 'POST':
        form = SavingsAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.member = member
            # Ensure this function is defined or imported
            account.account_number = generate_account_number()
            account.current_balance = 0.0
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('account_detail', account_id=account.id)
    else:
        form = SavingsAccountForm()

    return render(request, 'accounts/create_account.html', {
        'form': form,
        'member': member
    })


@login_required
def account_detail(request, account_id):
    account = get_object_or_404(SavingsAccount, id=account_id)
    if request.user != account.member.user:
        raise PermissionDenied
    transactions = Transaction.objects.filter(
        account=account).order_by('-transaction_date')
    return render(request, 'accounts/account_detail.html', {
        'account': account,
        'transactions': transactions
    })


@login_required
@permission_required('accounts.add_transaction', raise_exception=True)
def deposit(request, account_id):
    account = get_object_or_404(SavingsAccount, id=account_id)

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.transaction_type = 'DEP'
            transaction.processed_by = request.user
            transaction.reference_number = generate_account_ref()

            # Update account balance
            account.current_balance += transaction.amount

            # Save both transaction and account
            transaction.save()
            account.save()

            messages.success(request, 'Deposit successful!')
            return redirect('account_detail', account_id=account.id)
    else:
        form = DepositForm(initial={'account': account})

    return render(request, 'accounts/transaction_form.html', {
        'form': form,
        'account': account,
        'transaction_type': 'Deposit'
    })


def create_account(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.member = request.user.member  # Or get member from session
            account.save()  # Account number generated in pre_save signal
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountCreationForm()
    return render(request, 'accounts/create.html', {'form': form})


def generate_account_ref():
    """Generates a unique account reference number"""
    return f"ACC-{int(time.time())}"


def details(request, id):
    return HttpResponse(f"Details page for member with ID {id}")
 # Example implementation

# Similar view for withdrawals
# Helper functions would be in a separate utils.py


def generate_account_number():
    """Generates a unique account number"""
    return f"SAV-{int(time.time())}"
# Create your views here.


def transaction_history(request, account_id):
    account = get_object_or_404(SavingsAccount, id=account_id)

    # Permission check
    if request.user != account.member.user:
        return HttpResponseForbidden("You don't have permission to view these transactions")

    # Get all transactions and paginate
    transactions_list = Transaction.objects.filter(
        account=account
    ).select_related('processed_by').order_by('-transaction_date')

    paginator = Paginator(transactions_list, 10)  # Show 10 per page
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)

    context = {
        'account': account,
        'transactions': transactions
    }
    return render(request, 'accounts/transaction_history.html', context)
