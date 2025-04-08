from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username}: {self.description} - ${self.amount} on {self.date}"

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