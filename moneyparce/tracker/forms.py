from django import forms
from django import forms
from django import forms
from django.db.models import Q # Import Q
from django.contrib.auth.models import User # Import User
from .models import Transaction, Budget, Category
from . import models # Import models for Q object usage

class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(), # Initial empty queryset
        required=False,
        empty_label="-- Select Category --"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) # Get the user passed from the view
        super(TransactionForm, self).__init__(*args, **kwargs)
        if user:
            # Filter categories for the specific user OR global categories (user=None)
            self.fields['category'].queryset = Category.objects.filter(
                Q(user=user) | Q(user__isnull=True)
            )

    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'date', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.TextInput(attrs={'placeholder': 'e.g., Grocery shopping'}),
        }

class BudgetForm(forms.ModelForm):
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    month = forms.ChoiceField(choices=MONTH_CHOICES)
    monthly_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0'})
    )

    class Meta:
        model = Budget
        fields = ['monthly_amount', 'month']

class EditBudgetForm(forms.ModelForm):
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    month = forms.ChoiceField(choices=MONTH_CHOICES)
    monthly_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0'})
    )

    class Meta:
        model = Budget
        fields = ['monthly_amount', 'month']

# New form for adding categories
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Groceries, Utilities'})
        }
