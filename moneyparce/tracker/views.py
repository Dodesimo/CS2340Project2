from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm

@login_required
def dashboard_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/dashboard.html', {'transactions': transactions})

@login_required
def add_transaction_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('/')
    else:
        form = TransactionForm()
    return render(request, 'tracker/add_transaction.html', {'form': form})
