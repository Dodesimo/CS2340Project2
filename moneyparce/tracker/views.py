from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q # Import Q for complex lookups
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django import forms # Import forms module
from .models import Transaction, TransactionSummary, Budget
from .models import Transaction, TransactionSummary, Budget, Category # Add Category import
from .forms import TransactionForm, BudgetForm, CategoryForm # Add CategoryForm import
from .utils import generate_daily_transaction_summary
from datetime import datetime, timedelta
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import io


@login_required
def add_budget_view(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()

            return redirect('/')
    else:
        form = BudgetForm()
    return render(request, 'tracker/add_budget.html', {'form': form})

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

    all_budgets = Budget.objects.filter(user=request.user).order_by('-month')



    context = {
        'transactions': all_transactions,
        'today_transactions': today_transactions,
        'today_summary': summary,
        'recent_summaries': recent_summaries,
        'budgets': all_budgets,
    }
    
    return render(request, 'tracker/dashboard.html', context)

@login_required
def manage_categories_view(request):
    CategoryFormSet = forms.formset_factory(CategoryForm, extra=1) # Allow adding one new category at a time
    user_categories = Category.objects.filter(Q(user=request.user) | Q(user__isnull=True)).order_by('name')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            # Check if category already exists for this user or globally
            existing_category = Category.objects.filter(
                Q(name__iexact=category_name) & (Q(user=request.user) | Q(user__isnull=True))
            ).first()
            if not existing_category:
                category = form.save(commit=False)
                category.user = request.user # Assign category to the current user
                category.save()
                # Optionally add a success message here
                return redirect('tracker:manage_categories')
            else:
                # Optionally add an error message here (category already exists)
                form.add_error('name', 'A category with this name already exists.')
        # If form is invalid or category exists, re-render with errors
        context = {
            'form': form, # Pass the form with errors back
            'categories': user_categories
        }
        return render(request, 'tracker/manage_categories.html', context)

    else:
        form = CategoryForm() # Empty form for GET request

    context = {
        'form': form,
        'categories': user_categories
    }
    return render(request, 'tracker/manage_categories.html', context)

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
        # Pass the user to the form's __init__ method
        form = TransactionForm(user=request.user)
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
    
@login_required
def generate_pdf(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    total_spent = sum(t.amount for t in transactions)

    template = get_template("tracker/pdf_template.html")
    html = template.render({
        "transactions": transactions,
        "total_spent": total_spent,
        "request": request,  # Include this so you can still access request.user in the template
    })

    result = io.BytesIO()
    pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=result)

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="spending_report.pdf"'
    return response

@login_required
def example_budgets_view(request):
    """
    Displays example budget templates to the user.
    """
    example_budgets = [
        {
            'name': 'Student Budget (Monthly)',
            'description': 'A basic budget for a student living off-campus.',
            'categories': [
                {'name': 'Housing (Rent/Dorm)', 'amount': 800},
                {'name': 'Food (Groceries & Dining Out)', 'amount': 400},
                {'name': 'Transportation (Gas/Public Transit)', 'amount': 100},
                {'name': 'Tuition/Fees', 'amount': 500}, # Example, adjust as needed
                {'name': 'Books & Supplies', 'amount': 100},
                {'name': 'Personal Care', 'amount': 50},
                {'name': 'Entertainment', 'amount': 100},
                {'name': 'Savings', 'amount': 50},
            ],
            'total': 2100
        },
        {
            'name': '50/30/20 Rule Example (Monthly Income: $4000)',
            'description': 'Allocate 50% to Needs, 30% to Wants, 20% to Savings/Debt.',
            'categories': [
                {'name': 'Needs (50%)', 'amount': 2000, 'details': 'Rent/Mortgage, Utilities, Groceries, Insurance, Transportation, Min. Debt Payments'},
                {'name': 'Wants (30%)', 'amount': 1200, 'details': 'Dining Out, Hobbies, Entertainment, Shopping, Travel'},
                {'name': 'Savings/Debt (20%)', 'amount': 800, 'details': 'Emergency Fund, Retirement, Extra Debt Payments, Investments'},
            ],
            'total': 4000
        },
        {
            'name': 'Zero-Based Budget Example (Monthly Income: $3500)',
            'description': 'Every dollar has a job. Income minus Expenses equals zero.',
            'categories': [
                {'name': 'Income', 'amount': 3500},
                {'name': 'Rent/Mortgage', 'amount': -1200},
                {'name': 'Utilities', 'amount': -150},
                {'name': 'Groceries', 'amount': -400},
                {'name': 'Gas/Transportation', 'amount': -150},
                {'name': 'Insurance', 'amount': -100},
                {'name': 'Phone/Internet', 'amount': -100},
                {'name': 'Dining Out', 'amount': -200},
                {'name': 'Entertainment', 'amount': -150},
                {'name': 'Personal Spending', 'amount': -200},
                {'name': 'Savings', 'amount': -500},
                {'name': 'Debt Payment', 'amount': -350},
            ],
            'total': 0 # Should balance to zero
        }
    ]
    context = {
        'example_budgets': example_budgets
    }
    return render(request, 'tracker/example_budgets.html', context)
