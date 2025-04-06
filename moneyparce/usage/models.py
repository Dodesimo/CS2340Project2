from django.db import models
from django.contrib.auth.models import User

# Stores login event with timestamp
class LoginEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} logged in at {self.timestamp}"

# Proxy model to generate a sidebar admin link for the custom usage report
class UsageReportProxy(User):
    class Meta:
        proxy = True
        verbose_name = "📈 Usage Report"
        verbose_name_plural = "📈 Usage Report"
