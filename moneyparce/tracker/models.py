from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Optional: Link categories to users or make them global
    name = models.CharField(max_length=100, unique=True) # Ensure category names are unique

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories" # Correct pluralization in admin

class SavingTip(models.Model):
    tip = models.TextField()
    category = models.CharField(max_length=50)  # e.g., 'Food', 'Transportation', 'Shopping'
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ])
    potential_savings = models.CharField(max_length=100)  # e.g., '$5-10 per week'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.tip[:50]}..."

    class Meta:
        ordering = ['-created_at']

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    # Ensure this line exists and is correct
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.description} - {self.date}"

class TransactionSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    summary_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username}'s summary for {self.date}"

class TransactionReportProxy(User):
    class Meta:
        proxy = True
        verbose_name = "💳 Transaction Report"
        verbose_name_plural = "💳 Transaction Report"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DecimalField(max_digits=4, decimal_places=0)
    year = models.DecimalField(max_digits=4, decimal_places=0, default=timezone.now().year)

    def __str__(self):
        return f"{self.user.username}: {self.monthly_amount} for {self.month}/{self.year}"

    def get_current_spending(self):
        """Calculate total spending for the budget's month"""
        return Transaction.objects.filter(
            user=self.user,
            date__year=self.year,
            date__month=self.month
        ).aggregate(total=Sum('amount'))['total'] or 0

    def get_spending_percentage(self):
        """Calculate spending as a percentage of budget"""
        current_spending = self.get_current_spending()
        if self.monthly_amount > 0:
            return float((current_spending / self.monthly_amount) * 100)
        return 0.0

    def get_remaining_amount(self):
        """Calculate remaining budget amount"""
        return float(self.monthly_amount) - float(self.get_current_spending())

class BudgetNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Budget Alert for {self.user.username} - {self.budget.month}/{self.budget.monthly_amount}"

    class Meta:
        ordering = ['-created_at']