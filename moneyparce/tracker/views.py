from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Transaction, TransactionSummary
from .forms import TransactionForm
from .utils import generate_daily_transaction_summary
from datetime import datetime, timedelta

@login_required
def dashboard_view(request):
    today = timezone.now().date()
    
    all_transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    today_transactions = all_transactions.filter(date=today)
    
    summary, created = TransactionSummary.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={'summary_text': 'Generating summary...'}
    )
    
    if created or summary.summary_text == 'Generating summary...':
        summary_text = generate_daily_transaction_summary(today_transactions, today)
        summary.summary_text = summary_text
        summary.save()
    
    recent_summaries = TransactionSummary.objects.filter(
        user=request.user,
        date__gte=today - timedelta(days=7)
    ).order_by('-date')
    
    context = {
        'transactions': all_transactions,
        'today_transactions': today_transactions,
        'today_summary': summary,
        'recent_summaries': recent_summaries,
    }
    
    return render(request, 'tracker/dashboard.html', context)

@login_required
def add_transaction_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            
            today = timezone.now().date()
            if transaction.date == today:
                summary, created = TransactionSummary.objects.get_or_create(
                    user=request.user,
                    date=today,
                    defaults={'summary_text': 'Generating summary...'}
                )
                
                today_transactions = Transaction.objects.filter(
                    user=request.user,
                    date=today
                )
                summary_text = generate_daily_transaction_summary(today_transactions, today)
                summary.summary_text = summary_text
                summary.save()
            
            return redirect('/')
    else:
        form = TransactionForm()
    return render(request, 'tracker/add_transaction.html', {'form': form})

@login_required
def regenerate_summary_view(request, date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        transactions = Transaction.objects.filter(
            user=request.user,
            date=date
        )
        
        summary_text = generate_daily_transaction_summary(transactions, date)
        
        summary, created = TransactionSummary.objects.update_or_create(
            user=request.user,
            date=date,
            defaults={'summary_text': summary_text}
        )
        
        return redirect('/')
    except ValueError:
        return redirect('/')
