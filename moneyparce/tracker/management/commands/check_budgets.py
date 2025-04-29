from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from tracker.models import Budget, BudgetNotification
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings # To potentially get sender email address

# Define spending thresholds (e.g., 80% and 100%)
SPENDING_THRESHOLDS = [Decimal('0.80'), Decimal('1.00')]

class Command(BaseCommand):
    help = 'Checks user budgets and sends notifications if spending thresholds are met.'

    def handle(self, *args, **options):
        self.stdout.write('Starting budget check...')
        current_year = timezone.now().year
        current_month = timezone.now().month

        users = User.objects.all()
        notifications_created = 0

        for user in users:
            # Get budgets for the current month and year
            budgets = Budget.objects.filter(user=user, month=current_month)
            # Assuming 'month' field in Budget stores the month number (1-12)
            # If 'month' stores something else, this filter needs adjustment.
            # Also, need to consider the year if budgets span multiple years.
            # Let's refine the Budget model or query if necessary.
            # For now, assuming 'month' is the current month number and we check for the current year implicitly via transactions.

            for budget in budgets:
                spending_percentage_decimal = budget.get_spending_percentage() / Decimal('100.0')
                budget_amount = budget.monthly_amount
                current_spending = budget.get_current_spending()

                for threshold in SPENDING_THRESHOLDS:
                    # Check if spending exceeds the current threshold
                    if spending_percentage_decimal >= threshold:
                        # Check if a notification for this budget *at or above this threshold* has already been sent this month
                        existing_notification = BudgetNotification.objects.filter(
                            user=user,
                            budget=budget,
                            created_at__year=current_year,
                            created_at__month=current_month,
                            # Simple check: message contains the threshold percentage
                            message__icontains=f'{int(threshold * 100)}%'
                        ).exists()

                        if not existing_notification:
                            percentage_display = int(threshold * 100)
                            message = f"Alert: You have spent ${current_spending:.2f}, which is {percentage_display}% or more of your ${budget_amount:.2f} budget for month {int(budget.month)}."
                            
                            BudgetNotification.objects.create(
                                user=user,
                                budget=budget,
                                message=message
                            )
                            notifications_created += 1
                            self.stdout.write(f'Created notification for {user.username} - Budget {budget.id} at {percentage_display}%')

                            # Send email notification
                            if user.email: # Check if user has an email address
                                subject = f'Budget Alert: {percentage_display}% Spending Reached'
                                email_message = f"""Hi {user.username},

You have spent ${current_spending:.2f}, which is {percentage_display}% or more of your ${budget_amount:.2f} budget for month {int(budget.month)}.

Regards,
MoneyParce Team"""
                                try:
                                    send_mail(
                                        subject,
                                        email_message,
                                        settings.DEFAULT_FROM_EMAIL, # Ensure DEFAULT_FROM_EMAIL is set in settings.py
                                        [user.email],
                                        fail_silently=False,
                                    )
                                    self.stdout.write(f'Sent email alert to {user.email}')
                                except Exception as e:
                                    self.stderr.write(self.style.ERROR(f'Failed to send email to {user.email}: {e}'))
                            else:
                                self.stdout.write(f'User {user.username} has no email address configured for alerts.')

                            # Optional: Break after sending one notification per budget check cycle if desired
                            # break # Uncomment if you only want one notification per budget per run, even if multiple thresholds are crossed

        self.stdout.write(self.style.SUCCESS(f'Budget check complete. Created {notifications_created} notifications.'))