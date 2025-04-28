from django.contrib import admin
from django.template.response import TemplateResponse
from django.db.models import Sum
from .models import Transaction, TransactionReportProxy
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
from .models import Transaction, TransactionSummary, Budget, Category # Import Category

@admin.register(TransactionReportProxy)
class TransactionReportAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        start_date = request.GET.get('start', (now() - timedelta(days=30)).date().isoformat())
        end_date = request.GET.get('end', now().date().isoformat())
        user_id = request.GET.get('user')

        users = User.objects.all()
        transactions = Transaction.objects.filter(date__range=[start_date, end_date])

        if user_id:
            transactions = transactions.filter(user__id=user_id)

        summary = transactions.values('user__username') \
                              .annotate(total=Sum('amount')) \
                              .order_by('-total')

        extra_context = extra_context or {}
        extra_context.update({
            'title': 'Transaction Report',
            'transactions': transactions.order_by('-date'),
            'summary': summary,
            'users': users,
            'start': start_date,
            'end': end_date,
            'selected_user': int(user_id) if user_id else None
        })

        return TemplateResponse(request, "admin/transaction_report.html", extra_context)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user') # Adjust if user link is added/removed
    search_fields = ('name',)
    # list_filter = ('user',) # Add if user link exists and filtering is desired

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'description', 'date', 'category') # Add 'category'
    list_filter = ('user', 'date', 'category') # Add 'category'
    search_fields = ('description', 'user__username')
    date_hierarchy = 'date'

admin.site.register(TransactionSummary)
admin.site.register(Budget)
