from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Optional: Link categories to users or make them global
    name = models.CharField(max_length=100, unique=True) # Ensure category names are unique

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories" # Correct pluralization in admin

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

    def __str__(self):
        return f"{self.user.username}: {self.monthly_amount} for the month of {self.month}"