from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username}: {self.description} - ${self.amount} on {self.date}"

# For custom admin report access
class TransactionReportProxy(User):
    class Meta:
        proxy = True
        verbose_name = "💳 Transaction Report"
        verbose_name_plural = "💳 Transaction Report"
