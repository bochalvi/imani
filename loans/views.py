from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Loan, Repayment
from .forms import loanApplicationForm, repaymentForm


@login_required
def apply_loan(request):
    if request.method == 'POST':
        form = loanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.borrower = request.user
            loan.save()
            messages.success(
                request, 'Loan application submitted successfully.')
            return redirect('loan_detail', loan_id=loan.id)
    else:
        form = loanApplicationForm()
    return render(request, 'loans/apply_loan.html', {'form': form})


@login_required
def loan_list(request):
    loans = Loan.objects.filter(borrower=request.user).order_by('-created_at')
    if not loans:
        messages.info(request, 'You have no loans.')
    return render(request, 'loans/loan_list.html', {'loans': loans})


@login_required
def loan_detail(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, borrower=request.user)
    repayments = Repayment.objects.filter(loan=loan).order_by('-payment_date')
    form = repaymentForm()

    if request.method == 'POST':
        form = repaymentForm(request.POST)
        if form.is_valid():
            repayment = form.save(commit=False)
            repayment.loan = loan
            if repayment.amount > loan.balance:
                messages.error(
                    request, f'Amount exceeds loan balance (Kshs{loan.balance:.2f}).')
            else:
                repayment.save()
                messages.success(request, 'payment made successfully.')
                return redirect('loans:loan_detail', loan_id=loan.id)
        else:
            form = repaymentForm()

    context = {
        'loan': loan,
        'repayments': repayments,
        'form': form,
        'balance': loan.balance,
        'next_payment': loan.monthly_payment,
    }
    return render(request, 'loans/loan_detail.html', context)


# Create your views here.
